from .multinomial_logit import MultinomialLogit
from .mixed_logit import MixedLogit
from .latent_class_model import LatentClassModel
from .latent_class_mixed_model import LatentClassMixedModel
import numpy as np
# import pandas as pd
import time
import datetime
import matplotlib.pyplot as plt
import sys
import math
# from matplotlib.backends.backend_pdf import PdfPages

# TODO: global vars up here
# boxc_l is the list of suffixes used to denote manually transformed variables
boxc_l = ['L1', 'L2']  # ['L1','L2','L3']
l1 = np.log
l2 = 0.5

# TODO! INCLUDE RANDOM JUPYTER NOTEBOOK CODE IN FLOW


class Search():
    def __init__(self, dist=None, code_name="abc", avail=None, weights=None,
                 varnames=None, df=None, df_test=None, choice_set=None,
                 choice_var=None, test_choice=None,
                 alt_var=None, choice_id=None, ind_id=None, isvarnames=None,
                 asvarnames=None, trans_asvars=None, ftol=1e-5, gtol=1e-5,
                 latent_class=False, num_classes=2, maxiter=200, verbose=0,
                 multi_objective=False, p_val=0.05, Chosen_alts_test=None,
                 test_chid=None, test_ind_id=None,
                 test_alt_var=None):
        # TODO? GOOD ARANGING AND DESCRIPTION OF INIT PARAMS
        self.dist = dist  # List of random distributions to select from
        self.code_name = code_name
        self.current_date = datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
        self.avail = avail
        self.weights = weights
        self.varnames = varnames
        self.df = df
        self.df_test = df_test
        self.choice_set = choice_set
        self.choice_var = choice_var
        self.test_choice = test_choice
        self.alt_var = alt_var
        self.choice_id = choice_id
        self.ind_id = ind_id

        if isvarnames is None:
            isvarnames = []
        self.isvarnames = isvarnames

        if asvarnames is None:
            asvarnames = []
        self.asvarnames = asvarnames

        self.trans_asvars = trans_asvars
        self.ftol = ftol
        self.gtol = gtol
        self.latent_class = latent_class
        self.num_classes = num_classes
        self.maxiter = maxiter
        self.verbose = verbose
        self.test_av = None  # TODO?
        self.test_weight_var = None  # TODO?
        self.multi_objective = multi_objective
        self.p_val = p_val
        self.test_chid = test_chid  # TODO? Handle automatically?
        self.test_ind_id = test_ind_id
        self.test_alt_var = test_alt_var

        self.val_share = 0.25  # TODO?
        if Chosen_alts_test is None:
            try:
                Chosen_alts_test = df_test.query('choice == True')['alt']
            except Exception:
                Chosen_alts_test = df_test.query('CHOICE == True')['alt']

        self.obs_freq = (np.array(Chosen_alts_test.value_counts().
                         values.tolist()))/(df_test.shape[0]/len(choice_set))

    def prespec_features(self, ind_psasvar, ind_psisvar, ind_pspecdist,
                         ind_psbcvar, ind_pscorvar, isvarnames, asvarnames):
        """
        Generates lists of features that are predetermined by the modeller for
        the model development
        Inputs:
        (1) ind_psasvar - indicator list for prespecified asvars
        (2) ind_psisvar - indicator list for prespecified isvars
        (3) ind_pspecdist - indicator list for vars with prespecified coefficient distribution
        (4) ind_psbcvar - indicator list for vars with prespecified transformation
        (5) ind_pscorvar - indicator list for vars with prespecified correlation
        """
        # prespecified alternative-specific variables
        ps_asvar_pos = [i for i, x in enumerate(ind_psasvar) if x == 1]
        ps_asvars = [var for var in asvarnames if asvarnames.index(var) in ps_asvar_pos]

        # prespecified individual-specific variables
        ps_isvar_pos = [i for i, x in enumerate(ind_psisvar) if x == 1]
        ps_isvars = [var for var in isvarnames if isvarnames.index(var) in ps_isvar_pos]

        # prespecified coeff distributions for variables
        ps_rvar_ind = dict(zip(asvarnames, ind_pspecdist))
        ps_rvars = {k: v for k, v in ps_rvar_ind.items() if v != "any"}

        # prespecified non-linear transformed variables
        ps_bcvar_pos = [i for i, x in enumerate(ind_psbcvar) if x == 1]
        ps_bcvars = [var for var in asvarnames if asvarnames.index(var) in ps_bcvar_pos]

        # prespecified correlated variables
        ps_corvar_pos = [i for i, x in enumerate(ind_pscorvar) if x == 1]
        ps_corvars = [var for var in asvarnames if asvarnames.index(var) in ps_corvar_pos]

        return(ps_asvars, ps_isvars, ps_rvars, ps_bcvars, ps_corvars)

    def avail_features(self, asvars_ps, isvars_ps, rvars_ps, bcvars_ps,
                       corvars_ps, isvarnames, asvarnames):
        """
        Generates lists of features that are availbale to select from for model development
        Inputs:
        (1) asvars_ps - list of prespecified asvars
        (2) isvars_ps - list of prespecified isvars
        (3) rvars_ps - list of vars and their prespecified coefficient distribution
        (4) bcvars_ps - list of vars that include prespecified transformation
        (5) corvars_ps - list of vars with prespecified correlation
        """
        # available alternative-specific variables for selection
        avail_asvars = [var for var in asvarnames if var not in asvars_ps]

        # available individual-specific variables for selection
        avail_isvars = [var for var in isvarnames if var not in isvars_ps]

        # available variables for coeff distribution selection
        avail_rvars = [var for var in asvarnames if var not in rvars_ps.keys()]

        # available alternative-specific variables for transformation
        avail_bcvars = [var for var in asvarnames if var not in bcvars_ps]

        # available alternative-specific variables for correlation
        avail_corvars = [var for var in asvarnames if var not in corvars_ps]

        return (avail_asvars, avail_isvars, avail_rvars, avail_bcvars, avail_corvars)

    def df_coeff_col(self, seed, dataframe, test_df, names_asvars,
                     choiceset, var_alt):
        """
        This function creates dummy dataframe columns for variables,
        which are randomly selected to be estimated with
        alternative-specific coefficients.
        Inputs: random seed - int
                dataframe - pd.dataframe
                asvars - list of variable names to be considered
                choise_set - list of available alternatives
                var_alt - dataframe column consisting of alternative variable
        Output: List of as variables considered for model development
        """
        np.random.seed(seed)
        random_matrix = np.random.randint(0, 2, len(names_asvars))
        asvars_new = []
        alt_spec_pos_str = [str(var) for var in names_asvars if
                            random_matrix[names_asvars.index(var)] == 1]
        for i in alt_spec_pos_str:
            for j in choiceset:
                # TODO?: SAVE THIS PROPERLY?
                dataframe[i + '_' + j] = dataframe[i]*(var_alt == j)
                test_df[i + '_' + j] = test_df[i]*(var_alt == j)
                asvars_new.append(i + '_' + j)
                # print("asvars_new",asvars_new)
    
        asvars_new.extend([str(integer) for integer in names_asvars
                           if random_matrix[names_asvars.index(integer)] == 0])
        # print ("features after df_coeff_col", asvars_new)
        return(asvars_new)
        # TODO? OLD CODE - CONFIRM CHANGE?
        # np.random.seed(seed)
        # random_matrix = np.random.randint(0, 2, len(names_asvars))
        # asvars_new = []
        # alt_spec_pos_str = [str(var) for var in names_asvars
        #                     if random_matrix[names_asvars.index(var)] == 1]
        # for i in alt_spec_pos_str:
        #     for j in choiceset:
        #         dataframe[i + '_' + j] = dataframe[i]*(var_alt == j)
        #         self.df_test[i + '_' + j] = self.df_test[i]*(var_alt == j)
        #         asvars_new.append(i + '_' + j)

        # asvars_new.extend([str(integer) for integer in names_asvars
        #                    if random_matrix[names_asvars.index(integer)] ==0])

        # # create interaction variables
        # interaction_asvars = []
        # interaction_isvars = []
        # if len(asvars_new) > 0:
        #     interaction_asvars = np.random.choice(asvars_new, 1)

        # if len(names_isvars) > 0:
        #     interaction_isvars = np.random.choice(names_isvars, 1)
        # # TODO: what is this?
        # new_interaction_varname = []
        # if len(interaction_isvars) > 0 and len(interaction_asvars) > 0:
        #     new_interaction_varname = interaction_isvars[0] + "_" + \
        #         interaction_asvars[0]
        #     asvars_new.append(new_interaction_varname)
        #     dataframe[new_interaction_varname] = \
        #         dataframe[interaction_asvars[0]] * \
        #         dataframe[interaction_isvars[0]]

        # # Remove redundant isvar and asvar
        # asvars_new = [var for var in asvars_new
        #               if var not in interaction_asvars]
        # isvars_new = [var for var in names_isvars
        #               if var not in interaction_isvars]

        # return(asvars_new, isvars_new)

    # Removing redundancy if the same variable is included in the model with and without transformation
    # or with a combination of alt-spec and generic coefficients
    def remove_redundant_asvars(self, asvar_list, transasvars, seed, asvarnames):
        redundant_asvars = [s for s in asvar_list if any(xs in s for xs in transasvars)]
        unique_vars = [var for var in asvar_list if var not in redundant_asvars]
        np.random.seed(seed)
        # When transformations are not applied, the redundancy is created if a variable has both generic & alt-spec co-effs
        if len(transasvars) == 0:
            gen_var_select = [var for var in asvar_list if var in asvarnames]
            alspec_final = [var for var in asvar_list if var not in gen_var_select]
        else:
            gen_var_select = []
            alspec_final = []
            for var in transasvars:
                redun_vars = [item for item in asvar_list if var in item]
                gen_var = [var for var in redun_vars if var in asvarnames]
                if gen_var:
                    gen_var_select.append(np.random.choice(gen_var))
                alspec_redun_vars = [item for item in asvar_list
                                     if var in item and item not in asvarnames]
                trans_alspec = [i for i in alspec_redun_vars
                                if any(l for l in boxc_l if l in i)]
                lin_alspec = [var for var in alspec_redun_vars
                              if var not in trans_alspec]
                if np.random.randint(2):
                    alspec_final.extend(lin_alspec)
                else:
                    alspec_final.extend(trans_alspec)
        np.random.seed(seed)
        if len(gen_var_select) and len(alspec_final) != 0:
            if np.random.randint(2):
                final_asvars = gen_var_select
                final_asvars.extend(unique_vars)
            else:
                final_asvars = alspec_final
                final_asvars.extend(unique_vars)

        elif len(gen_var_select) != 0:
            final_asvars = gen_var_select
            final_asvars.extend(unique_vars)
        else:
            final_asvars = alspec_final
            final_asvars.extend(unique_vars)

        return(list(dict.fromkeys(final_asvars)))

    def generate_sol(self, data, test_df, seed, asvars_avail, isvars_avail, rvars_avail,
                     transasvars, bcvars_avail, corvars_avail, asvars_ps,
                     isvars_ps, rvars_ps, bcvars_ps, corvars_ps, bctrans_ps,
                     cor_ps, intercept_ps, asvarnames, choice_set, alt_var):
        """
        Generates list of random model features and then includes modeller prespecifications
        Inputs:
        (1) seed - seed for random generators
        (2) asvars_avail - list of available asvars for random selection
        (3) isvars_avail - list of available isvars for random selection
        (4) rvars_avail - list of available vars for randomly selected coefficient distribution
        (5) bcvars_avail - list of available vars for random selection of transformation
        (6) corvars_avail - list of available vars for random selection of correlation
        ## Prespecification information
        (1) asvars_ps - list of prespecified asvars
        (2) isvars_ps - list of prespecified isvars
        (3) rvars_ps - list of vars and their prespecified coefficient distribution
        (4) bcvars_ps - list of vars that include prespecified transformation
        (5) corvars_ps - list of vars with prespecified correlation
        (6) bctrans_ps - prespecified transformation boolean
        (7) cor_ps - prespecified correlation boolean
        (8) intercept_ps - prespecified intercept boolean

        """

        np.random.seed(seed)
        ind_availasvar = []
        for i in range(len(asvars_avail)):
            ind_availasvar.append(np.random.randint(2))
        asvar_select_pos = [i for i, x in enumerate(ind_availasvar) if x == 1]
        asvars_1 = [var for var in asvars_avail if asvars_avail.index(var)
                    in asvar_select_pos]
        asvars_1.extend(asvars_ps)

        asvars_new = self.remove_redundant_asvars(asvars_1, transasvars, seed,
                                                  asvarnames)
        asvars = self.df_coeff_col(seed, data, test_df, asvars_new,
                                   choice_set, alt_var)

        # ind_availisvar = []
        # for i in range(len(isvars_avail)):
        #     ind_availisvar.append(np.random.randint(2))
        # isvar_select_pos = [i for i, x in enumerate(ind_availisvar) if x == 1]
        # isvars = [var for var in isvars_avail if isvars_avail.index(var) in isvar_select_pos]
        # isvars.extend(isvars_ps)

        # asvars, isvars = self.df_coeff_col(seed, data, test_df, asvars_new, isvars,
        #                                    choice_set, alt_var)

        r_dist = []
        avail_rvar = [var for var in asvars if var in rvars_avail]
        # TODO! RYAN TMP
        # avail_rvar = []
        for i in range(len(avail_rvar)):
            r_dist.append(np.random.choice(self.dist))

        rvars = dict(zip(avail_rvar, r_dist))
        rvars.update(rvars_ps)

        ind_availisvar = []
        for i in range(len(isvars_avail)):
            ind_availisvar.append(np.random.randint(2))
        isvar_select_pos = [i for i, x in enumerate(ind_availisvar) if x == 1]
        isvars = [var for var in isvars_avail if isvars_avail.index(var) in isvar_select_pos]
        isvars.extend(isvars_ps)

        rand_vars = {k: v for k, v in rvars.items() if v != "f" and k in asvars}
        r_dis = [dis for dis in self.dist if dis != "f"]
        for var in corvars_ps:
            if var in asvars and var not in rand_vars.keys():
                rand_vars.update({var: np.random.choice(r_dis)})

        if bctrans_ps is None:
            bctrans = bool(np.random.randint(2, size=1))
        else:
            bctrans = bctrans_ps

        if bctrans:
            ind_availbcvar = []
            for i in range(len(bcvars_avail)):
                ind_availbcvar.append(np.random.randint(2))
            bcvar_select_pos = [i for i, x in enumerate(ind_availbcvar) if x == 1]
            bcvars = [var for var in bcvars_avail if bcvars_avail.index(var) in bcvar_select_pos]
            bcvars.extend(bcvars_ps)
            bc_vars = [var for var in bcvars if var in asvars and var not in corvars_ps]
            # variables with random parameters cannot be estimated with lambda
            # TODO?? IS THIS RIGHT
            bc_vars = [var for var in bc_vars if var not in rand_vars.keys()]
        else:
            bc_vars = []

        if cor_ps is None:
            cor = bool(np.random.randint(2, size=1))
        else:
            cor = cor_ps

        if cor:
            ind_availcorvar = []
            for i in range(len(corvars_avail)):
                ind_availcorvar.append(np.random.randint(2))
            corvar_select_pos = [i for i, x in enumerate(ind_availcorvar)
                                 if x == 1]
            corvars = [var for var in corvars_avail if corvars_avail.index(var)
                       in corvar_select_pos]
            corvars.extend(corvars_ps)
            cor_vars = [var for var in corvars if var in rand_vars.keys()
                        and var not in bc_vars]
            if len(cor_vars) < 2:
                cor = False
                cor_vars = []
        else:
            cor_vars = []

        if intercept_ps is None:
            asc_ind = bool(np.random.randint(2, size=1))
        else:
            asc_ind = intercept_ps
        return(asvars, isvars, rand_vars, bc_vars, cor_vars, bctrans, cor,
               asc_ind)

    def fit_mnl(self, dat, test_df, as_vars, is_vars, bcvars, choice, alt,
                id_choice,
                test_choice, asc_ind, alt_var, avail=None, weights=None,
                iterations=200,
                ftol=1e-4, gtol=1e-4):
        """
        Estimates multinomial model for the generated solution
        Inputs:
        (1) dat in csv
        (2) as_vars: list of alternative-specific variables
        (3) is_vars: list of individual-specific variables
        (4) bcvars: list of box-cox variables
        (5) choice: df column with choice variable
        (6) alt: df column with alternative variables
        (7) id_choice: df column with choice situation id
        (8) asc_ind: boolean for fit_intercept
        """
        data = dat.copy()
        all_vars = as_vars + is_vars
        avail = avail or self.avail
        weights = weights or self.weights
        # print("all_vars inputs for mnl",all_vars)
        X = data[all_vars].values
        y = choice
        model = MultinomialLogit()
        model.fit(X, y, varnames=all_vars, isvars=is_vars, alts=alt_var,
                  ids=id_choice, fit_intercept=asc_ind,
                  transformation="boxcox", transvars=bcvars,
                  maxiter=self.maxiter, ftol=ftol, gtol=gtol, avail=avail,
                  weights=weights)
        rand_vars = {}
        cor_vars = []
        bc_vars = [var for var in bcvars if var not in self.isvarnames]
        print(model.summary())

        print("model convergence", model.convergence)

        # TODO? MOOF specific?
        # Validation
        X_test = test_df[all_vars].values
        y_test = test_choice.values
        # val = abs(model.loglikelihood - (model.validation_loglik(X_test, y_test)/val_share))
        val = model.loglikelihood - \
            (model.validation_loglik(X_test, y_test)/self.val_share)

        return(model.bic, val, as_vars, is_vars, rand_vars, bc_vars, cor_vars,
               model.convergence, model.pvalues, model.coeff_names)

    def fit_mxl(self, dat, test_df, as_vars, is_vars, rand_vars, bcvars, corvars,
                choice, alt, id_choice, id_val, test_choice,
                asc_ind, avail=None,
                weights=None, iterations=200, tol=1e-2, R=200):
        """
        Estimates the model for the generated solution
        Inputs:
        (1) dat: dataframe in csv
        (2) as_vars: list of alternative-specific variables
        (3) is_vars: list of individual-specific variables
        (4) bcvars: list of box-cox variables
        (5) choice: df column with choice variable
        (6) corvars: list of variables allowed to correlate
        (7) alt: df column with alternative variables
        (8) id_choice: df column with choice situation id
        (9) id_val: df column with individual id
        (10) asc_ind: boolean for fit_intercept
        """
        data = dat.copy()  # TODO?
        all_vars = as_vars + is_vars
        X = data[all_vars].values
        y = choice
        if corvars == []:
            corvars = False

        bcvars = [var for var in bcvars if var not in self.isvarnames]
        model = MixedLogit()
        model.fit(X, y, varnames=all_vars, alts=alt, isvars=is_vars,
                  ids=id_choice, panels=id_val, randvars=rand_vars,
                  n_draws=R, fit_intercept=asc_ind, correlation=corvars,
                  transformation="boxcox", transvars=bcvars,
                  maxiter=self.maxiter, avail=avail, ftol=tol, gtol=tol,
                  weights=weights)

        bic = model.bic
        def_vals = model.coeff_
        print(model.summary())
        conv = model.convergence
        pvals = model.pvalues
        coef_names = model.coeff_names

        print("model convergence", model.convergence)

        # Validation
        X_test = test_df[all_vars].values
        y_test = test_choice
        # val = abs(model.loglikelihood- (model.validation_loglik(X_test,
        #           y_test,panels=test_ind_id)/val_share))
        val = model.loglikelihood - (model.validation_loglik(X_test,
                                                             y_test.values,
                                                             panels=self.test_ind_id)
                                     / self.val_share)
        print("val", val)

        # MAE
        model = MixedLogit()
        model.fit(X_test, y_test, varnames=all_vars, alts=self.test_alt_var,
                  isvars=is_vars,
                  ids=self.test_chid, panels=self.test_ind_id,
                  randvars=rand_vars, n_draws=R,
                  fit_intercept=asc_ind, correlation=corvars,
                  transformation="boxcox",
                  transvars=bcvars, avail=self.test_av, maxiter=0,
                  init_coeff=def_vals, gtol=self.gtol,
                  weights=self.test_weight_var)

        # Calculating MAE

        # Choice frequecy obtained from estimated model applied on testing sample
        predicted_probabilities_val = model.pred_prob

        MAE = (1/len(self.choice_set))*(np.sum(abs(predicted_probabilities_val -
                                                   self.obs_freq)))
        print("MAE", MAE)

        return(bic, MAE, as_vars, is_vars, rand_vars, bcvars, corvars, conv,
               pvals, coef_names)

    def fit_lccm(self, dat, test_df, as_vars, is_vars, num_classes,
                 bcvars, choice, alt, id_choice, test_choice, asc_ind):
        """Estimates multinomial model for the generated solution.
        Inputs:
        (1) dat in csv
        (2) as_vars: list of alternative-specific variables
        (3) is_vars: list of individual-specific variables
        (4) num_classes: number of latent classes
        (5) bcvars: list of box-cox variables
        (6) choice: df column with choice variable
        (7) alt: df column with alternative variables
        (8) id_choice: df column with choice situation id
        (9) asc_ind: boolean for fit_intercept
        """
        print("estimating lccm")
        print('as_vars', as_vars)
        print('is_vars', is_vars)
    #     print('rand_vars', rand_vars)
        print('bcvars', bcvars)
    #     print('corvars', corvars)
        print('asc_ind', asc_ind)

        #     print("max_classes", max_classes)
        # data = dat.copy()
        all_vars = as_vars + is_vars
        # print("all_vars inputs for mnl",all_vars)
        X = dat[all_vars]
        y = choice
        model = LatentClassModel()
        if self.num_classes is None:
            optimal_num, model = \
                model.optimal_class_fit(X, y, varnames=all_vars,
                                        isvars=is_vars,
                                        alts=self.alt_var, ids=id_choice,
                                        fit_intercept=asc_ind,
                                        transformation="boxcox",
                                        transvars=bcvars,
                                        maxiter=self.maxiter,
                                        gtol=self.gtol,
                                        avail=self.avail,
                                        weights=self.weights,
                                        num_classes=self.num_classes)
        else:
            print('num_classes', self.num_classes)
            model.fit(X, y, varnames=all_vars, isvars=is_vars,
                      #   class_params_spec=class_params_spec,  # TODO!
                      #   member_params_spec=member_params_spec, # TODO!
                      num_classes=self.num_classes, alts=self.alt_var,
                      ids=id_choice, fit_intercept=asc_ind,
                      transformation="boxcox", transvars=bcvars,
                      maxiter=self.maxiter, gtol=self.gtol, avail=self.avail,
                      weights=self.weights)
        bic = model.bic
        # def_vals = model.coeff_
        rand_vars = {}
        cor_vars = []
        bc_vars = [var for var in bcvars if var not in self.isvarnames]
        print(model.summary())
        conv = model.convergence
        pvals = model.pvalues
        coef_names = model.coeff_names
        print("model convergence", model.convergence)

        # Validation
        X_test = self.df_test[all_vars].values
        y_test = self.df_test['choice']
        val = model.loglikelihood - (model.validation_loglik(X_test,
                                                             y_test.values)
                                     / self.val_share)
        print("val", val)

        # Choice frequecy obtained from estimated model applied on testing sample
        predicted_probabilities_val = model.pred_prob

        MAE = (1/len(self.choice_set))*(np.sum(abs(predicted_probabilities_val
                                                   - self.obs_freq)))
        print("MAE", MAE)

        return(bic, MAE, as_vars, is_vars, rand_vars, bc_vars, cor_vars,
               conv, pvals, coef_names)

    def fit_lccmm(self, dat, test_df, as_vars, is_vars, num_classes, rand_vars,
                  bcvars, corvars, choice, alt, id_choice, id_val, test_choice,
                  asc_ind):
        # print("estimating lccmm")
        # print('as_vars', as_vars)
        # print('is_vars', is_vars)
        # print('rand_vars', rand_vars)
        # print('bcvars', bcvars)
        # print('corvars', corvars)
        # print('asc_ind', asc_ind)
        R = 200  # TODO CHECK - set to Reduce computation
        # data = dat.copy()
        # is_vars = []  # TODO! TEMP FIX AS ISVARS BROKEN WITH LCCM
        all_vars = as_vars + is_vars
        X = dat[all_vars]
        y = choice
        if corvars == []:
            corvars = False
        bcvars = [var for var in bcvars if var not in self.isvarnames]
        model = LatentClassMixedModel()
        if self.num_classes is None:
            optimal_num, model = model.fit(X, y, varnames=all_vars,
                                           alts=self.alt_var, isvars=is_vars,
                                           ids=id_choice, panels=id_val,
                                           randvars=rand_vars, n_draws=R,
                                           fit_intercept=asc_ind,
                                           correlation=corvars,
                                           transformation="boxcox",
                                           transvars=bcvars,
                                           maxiter=self.maxiter,
                                           avail=self.avail,
                                           gtol=self.gtol,
                                           weights=self.weights,
                                           grad=True,
                                           num_classes=self.num_classes)
        else:
            model.fit(X, y, varnames=all_vars, alts=self.alt_var,
                      isvars=is_vars, num_classes=self.num_classes,
                      ids=id_choice, panels=id_val,
                      randvars=rand_vars, n_draws=R,
                      fit_intercept=asc_ind, correlation=corvars,
                      transformation="boxcox", transvars=bcvars,
                      maxiter=self.maxiter, avail=self.avail,
                      gtol=self.gtol, weights=self.weights,
                      grad=True)
        bic = model.bic
        def_vals = model.coeff_
        print(model.summary())
        conv = model.convergence
        pvals = model.pvalues
        coef_names = model.coeff_names

        print("model convergence", model.convergence)

        # Validation
        X_test = test_df[all_vars].values
        y_test = test_choice
        # val = abs(model.loglikelihood- (model.validation_loglik(X_test,
        # y_test,panels=test_ind_id)/val_share))
        val = model.loglikelihood - \
            (model.validation_loglik(X_test,
                                     y_test.values,
                                     ids=self.df_test['id'])
             / self.val_share)
        print("val", val)
        # MAE

        # TODO: What's going on here?
        model = LatentClassMixedModel()

        model.fit(X_test, y_test, varnames=all_vars, alts=self.df_test['alt'],
                  isvars=is_vars, num_classes=self.num_classes,
                  ids=self.df_test['id'], panels=self.df_test['id'],
                  randvars=rand_vars, n_draws=R,
                  fit_intercept=asc_ind, correlation=corvars,
                  transformation="boxcox",
                  transvars=bcvars, avail=self.test_av, maxiter=0,
                  init_coeff=def_vals,  # TODO? weird saving?
                  gtol=self.gtol, weights=self.test_weight_var,
                  grad=True)

        # Calculating MAE

        # Choice frequecy obtained from estimated model applied on testing sample
        predicted_probabilities_val = model.pred_prob

        MAE = (1/len(self.choice_set))*(np.sum(abs(predicted_probabilities_val
                                                   - self.obs_freq)))
        print("MAE", MAE)

        return(bic, MAE, as_vars, is_vars, rand_vars, bcvars, corvars, conv,
               pvals, coef_names)

    def evaluate_objective_function(self, new_df, test_df, seed, as_vars,
                                    is_vars, rand_vars, bc_vars, cor_vars,
                                    choice, test_choice, alts, id_choice,
                                    id_val, asc_ind,
                                    ps_asvars, asvarnames, isvarnames,
                                    ps_isvars, ps_intercept, choice_set,
                                    ps_rvars, ps_corvars):
        """
        (1) Evaluates the objective function (estimates the model and BIC) for
        a given list of variables (estimates the model coefficeints, LL and BIC)
        (2) If the solution generated in (1) contains statistically insignificant variables,
        a new model is generated by removing such variables and the model is re-estimated
        (3) the functions returns estimated solution only if it converges
        Inputs: lists of variable names, individual specific variables,
        variables with random coefficients,
        name of the choice variable in df, list of alternatives, choice_id,
        individual_id(for panel data) and fit intercept bool
        """
        all_vars = as_vars + is_vars

        sol = [-10000000.0, 1.0, [], [], {}, [], [], False]
        convergence = False

        if not cor_vars:  # TODO! RYAN CHANGE CHECK
            cor_vars = []

        # Estimate model if input variables are present in specification
        if all_vars:
            iterations = 200  # iterations for MNL fit...
            print("features for round 1", as_vars, is_vars, rand_vars, bc_vars,
                  cor_vars, asc_ind)
            # TODO! INCLUDE DF TEST IN ALL MODELS
            if bool(rand_vars):
                if self.latent_class:
                    # TODO: better way of including num_classes
                    bic, val, asvars, isvars, randvars, bcvars, corvars, \
                        conv, sig, coefs = self.fit_lccmm(new_df,
                                                          self.df_test,
                                                          as_vars, is_vars, 2,
                                                          rand_vars, bc_vars,
                                                          cor_vars, choice,
                                                          alts, id_choice,
                                                          id_val,
                                                          self.test_choice,
                                                          asc_ind)
                else:
                    print("estimating an MXL model")
                    bic, val, asvars, isvars, randvars, bcvars, corvars, \
                        conv, sig, coefs = self.fit_mxl(new_df, self.df_test,
                                                        as_vars, is_vars,
                                                        rand_vars, bc_vars,
                                                        cor_vars,
                                                        choice, alts,
                                                        id_choice,
                                                        id_val,
                                                        self.test_choice,
                                                        asc_ind,
                                                        avail=self.avail)
            else:
                if self.latent_class:
                    bic, val, asvars, isvars, randvars, bcvars, corvars, \
                        conv, sig, coefs = self.fit_lccm(new_df, self.df_test,
                                                         as_vars, is_vars, 2,
                                                         bc_vars, choice, alts,
                                                         id_choice,
                                                         self.test_choice,
                                                         asc_ind)
                else:
                    print("estimating an MNL model")
                    bic, val, asvars, isvars, randvars, bcvars, corvars, \
                        conv, sig, coefs = self.fit_mnl(new_df, self.df_test,
                                                        as_vars, is_vars,
                                                        bc_vars, choice, alts,
                                                        id_choice,
                                                        self.test_choice,
                                                        asc_ind, alts,
                                                        self.avail,
                                                        self.weights,
                                                        iterations,
                                                        self.ftol,
                                                        self.gtol)  # TODO? ugly
            if conv:
                if not corvars:
                    corvars = []
                print("solution converged in first round")
                sol = [bic, val, asvars, isvars, randvars, bcvars, corvars,
                       asc_ind]
                convergence = conv
                if all(v for v in sig <= self.p_val):
                    print("solution has all sig-values in first  round")
                    return (sol, convergence)
                else:
                    while any([v for v in sig if self.p_val]):
                        print("solution consists insignificant coeffs")
                        # create dictionary of {coefficient_names: p_values}
                        p_vals = dict(zip(coefs, sig))
                        # print("p_vals =", p_vals)
                        r_dist = [dis for dis in self.dist if dis != 'f']  # list of random distributions
                        # create list of variables with insignificant coefficients
                        non_sig = [k for k, v in p_vals.items()
                                   if v > self.p_val]  # list of non-significant coefficient names
                        print("non-sig coeffs are", non_sig)
                        # keep only significant as-variables
                        asvars_round2 = [var for var in asvars if var not in non_sig]  # as-variables with significant p-vals
                        asvars_round2.extend(ps_asvars)
                        print("asvars_round2 for round 2", asvars_round2)
                        # replace non-sig alt-spec coefficient with generic coefficient
                        nsig_altspec = []
                        for var in asvarnames:
                            ns_alspec = [x for x in non_sig if x.startswith(var)]
                            nsig_altspec.extend(ns_alspec)
                            nsig_altspec_vars = [var for var in nsig_altspec
                                                 if var not in asvarnames]
                        print("nsig_altspec_vars", nsig_altspec_vars)

                        # Replacing non-significant alternative-specific coeffs with generic coeffs estimation
                        if nsig_altspec_vars:
                            gen_var = []
                            for i in range(len(nsig_altspec_vars)):
                                gen_var.extend(nsig_altspec_vars[i].split("_"))
                            gen_coeff = [var for var in asvarnames if var
                                         in gen_var]
                            if asvars_round2:
                                redund_vars = [s for s in gen_coeff if any(s
                                               in xs for xs in asvars_round2)]
                                print("redund_vars for round 2", redund_vars)
                                asvars_round2.extend([var for var in gen_coeff
                                                      if var not in redund_vars])
                                # rem_asvars = remove_redundant_asvars(asvars_round2,trans_asvars,seed)
                                print("asvars_round2 before removing redundancy", asvars_round2)
                                # rem_asvars = remove_redundant_asvars(asvars_round2,trans_asvars,seed)
                                # checking if remove_redundant_asvars is needed or not
                                rem_asvars = sorted(list(set(asvars_round2)))
                            else:
                                rem_asvars = gen_coeff
                        else:
                            rem_asvars = sorted(list(set(asvars_round2)))
                        print("rem_asvars =", rem_asvars)
                        # remove insignificant is-variables
                        ns_isvars = []
                        for isvar in isvarnames:
                            ns_isvar = [x for x in non_sig if
                                        x.startswith(isvar)]
                            ns_isvars.extend(ns_isvar)
                        remove_isvars = []
                        for i in range(len(ns_isvars)):
                            remove_isvars.extend(ns_isvars[i].split("."))

                        remove_isvar = [var for var in remove_isvars if var
                                        in isvars]
                        most_nsisvar = {x: remove_isvar.count(x) for x
                                        in remove_isvar}
                        rem_isvar = [k for k, v in most_nsisvar.items()
                                     if v == (len(choice_set)-1)]
                        isvars_round2 = [var for var in is_vars if var
                                         not in rem_isvar]  # individual specific variables with significant p-vals
                        isvars_round2.extend(ps_isvars)
                        # print("isvars_round2 =", isvars_round2)
                        rem_isvars = sorted(list(set(isvars_round2)))
                        # print("rem_isvars =", rem_isvars)

                        # remove intercept if not significant and not prespecified
                        ns_intercept = [x for x in non_sig if
                                        x.startswith('_intercept.')]  # non-significant intercepts
                        # print("ns_intercept =", ns_intercept)

                        new_asc_ind = asc_ind

                        if ps_intercept is None:
                            if len(ns_intercept) == len(choice_set)-1:
                                new_asc_ind = False
                        else:
                            new_asc_ind = ps_intercept

                        # print("new_asc_ind =", new_asc_ind)

                        # remove insignificant random coefficients

                        ns_sd = [x for x in non_sig if x.startswith('sd.')]  # non-significant standard deviations
                        ns_sdval = [str(i).replace('sd.', '') for i in ns_sd]  # non-significant random variables

                        # non-significant random variables that are not pre-included
                        remove_rdist = [x for x in ns_sdval if x not in
                                        ps_rvars.keys() or x not in rem_asvars]
                        # random coefficients for significant variables
                        rem_rand_vars = {k: v for k, v in randvars.items()
                                         if k in rem_asvars and k not in
                                         remove_rdist}
                        rem_rand_vars.update({k: v for k, v in ps_rvars.items()
                                              if k in rem_asvars and v != 'f'})
                        print("rem_rand_vars =", rem_rand_vars)
                        # including ps_corvars in the model if they are included in rem_asvars
                        for var in ps_corvars:
                            if var in rem_asvars and var not in rem_rand_vars.keys():
                                rem_rand_vars.update({var: np.random.choice(r_dist)})
                        # print("rem_rand_vars =", rem_rand_vars)
                        # remove transformation if not significant and non prespecified
                        ns_lambda = [x for x in non_sig if x.startswith('lambda.')]  # insignificant transformation coefficient
                        ns_bctransvar = [str(i).replace('lambda.', '')
                                         for i in ns_lambda]  # non-significant transformed var
                        rem_bcvars = [var for var in bcvars if var in
                                      rem_asvars and var not in ns_bctransvar
                                      and var not in ps_corvars]
                        # print("rem_bcvars =", rem_bcvars)

                        # remove insignificant correlation
                        ns_chol = [x for x in non_sig if x.startswith('chol.')]  # insignificant cholesky factor
                        ns_cors = [str(i).replace('chol.', '') for i in ns_chol]  # insignicant correlated variables
                        # create a list of variables whose correlation coefficient is insignificant
                        if ns_cors:
                            ns_corvar = []
                            for i in range(len(ns_cors)):
                                ns_corvar.extend(ns_cors[i].split("."))
                            most_nscorvars = {x: ns_corvar.count(x)
                                              for x in ns_corvar}
                            print(most_nscorvars)
                            # check frequnecy of variable names in non-significant coefficients
                            nscorvars = [k for k, v in most_nscorvars.items()
                                         if v >= int(len(corvars)*0.75)]
                            print(nscorvars)
                            nonps_nscorvars = [var for var in nscorvars
                                               if var not in ps_corvars]
                            # if any variable has insignificant correlation
                            # with all other variables, their correlation is
                            # removed from the solution
                            if nonps_nscorvars:
                                # list of variables allowed to correlate
                                rem_corvars = [var for var in
                                               rem_rand_vars.keys() if var
                                               not in nonps_nscorvars and
                                               var not in rem_bcvars]
                            else:
                                rem_corvars = [var for var in
                                               rem_rand_vars.keys() if var
                                               not in rem_bcvars]

                            # need atleast two variables in the list to
                            # estimate correlation coefficients
                            if len(rem_corvars) < 2:
                                rem_corvars = []
                        else:
                            rem_corvars = [var for var in corvars if var in
                                           rem_rand_vars.keys() and var not in
                                           rem_bcvars]
                            if len(rem_corvars) < 2:
                                rem_corvars = []

                        # print("rem_corvars =", rem_corvars)
                        # Evaluate objective function with significant feautures from round 1
                        # print("features for round2",rem_asvars,rem_isvars,
                        # rem_rand_vars,rem_bcvars,rem_corvars,new_asc_ind)

                        rem_alvars = rem_asvars + rem_isvars
                        if rem_alvars:
                            # print("remaining vars present")
                            if (set(rem_alvars) != set(all_vars) or
                                set(rem_rand_vars) != set(rand_vars) or
                                set(rem_bcvars) != set(bcvars) or
                                set(rem_corvars) != set(corvars) or
                                    new_asc_ind != asc_ind):
                                print("not same as round 1 model")
                            else:
                                print("model 2 same as round 1 model")
                                return(sol, convergence)

                            if bool(rem_rand_vars):
                                if self.latent_class:
                                    bic, val, asvars, isvars, randvars, \
                                        bcvars, corvars, conv, sig, coefs = \
                                            self.fit_lccmm(new_df,
                                                           self.df_test,
                                                           as_vars,
                                                           is_vars,
                                                           2,
                                                           rand_vars,
                                                           bc_vars,
                                                           cor_vars,
                                                           choice,
                                                           alts,
                                                           id_choice,
                                                           id_val,
                                                           self.test_choice,
                                                           asc_ind)
                                else:
                                    print("MXL model round 2")
                                    bic, val, asvars, isvars, randvars, bcvars, \
                                        corvars, conv, sig, coefs = \
                                            self.fit_mxl(new_df,
                                                         self.df_test,
                                                         rem_asvars,
                                                         rem_isvars,
                                                         rem_rand_vars,
                                                         rem_bcvars,
                                                         rem_corvars,
                                                         choice, alts,
                                                         id_choice,
                                                         id_val,
                                                         self.test_choice,
                                                         new_asc_ind,
                                                         avail=self.avail)
                            else:
                                if self.latent_class:
                                    bic, val, asvars, isvars, randvars, \
                                        bcvars, corvars, conv, sig, coefs = \
                                            self.fit_lccm(new_df, self.df_test,
                                                          rem_asvars,
                                                          rem_isvars,
                                                          2,
                                                          rem_bcvars,
                                                          choice,
                                                          alts,
                                                          id_choice,
                                                          self.test_choice,
                                                          asc_ind)
                                else:
                                    print("MNL model round 2")
                                    bic, val, asvars, isvars, randvars, bcvars, \
                                        corvars, conv, sig, coefs = \
                                            self.fit_mnl(new_df,
                                                         self.df_test,
                                                         rem_asvars,
                                                         rem_isvars,
                                                         rem_bcvars,
                                                         choice, alts,
                                                         id_choice,
                                                         self.test_choice,
                                                         new_asc_ind,
                                                         alts)

                            if conv:
                                sol = [bic, val, asvars, isvars, randvars,
                                       bcvars, corvars, new_asc_ind]
                                convergence = conv
                                if all([v for v in sig if v <= self.p_val]):
                                    break
                                    # return(sol,convergence)
                                # if only some correlation coefficients or
                                # intercept values are insignificant, we accept
                                # the solution
                                p_vals = dict(zip(coefs, sig))
                                non_sig = [k for k, v in p_vals.items()
                                           if v > self.p_val]
                                print("non_sig in round 2", non_sig)

                                sol[2] = [var for var in sol[2] if var not in
                                          non_sig or var in ps_asvars]  # keep only significant vars

                                # Update other features of solution based on sol[1]
                                sol[4] = {k: v for k, v in sol[4].items() if k in sol[2]}
                                sol[5] = [var for var in sol[5] if var in sol[2] and var not in ps_corvars]
                                sol[6] = [var for var in sol[6] if var in sol[4].keys and var not in sol[5]]

                                # fit_intercept = False if all intercepts are insignificant
                                if len([var for var in non_sig if var in
                                       ['_intercept.' + var for var
                                        in choice_set]]) == len(non_sig):
                                    if len(non_sig) == len(choice_set)-1:
                                        sol[-1] = False
                                        return(sol, convergence)

                                all_ns_int = [x for x in non_sig if x.startswith('_intercept.')]
                                all_ns_cors = [x for x in non_sig if x.startswith('chol.')]

                                all_ns_isvars = []
                                for isvar in isvarnames:
                                    ns_isvar = [x for x in non_sig if x.startswith(isvar)]
                                    all_ns_isvars.extend(ns_isvar)

                                irrem_nsvars = all_ns_isvars + all_ns_int + all_ns_cors
                                if all(nsv in irrem_nsvars for nsv in non_sig):
                                    print("non-significant terms cannot be further eliminated")
                                    return(sol, convergence)

                                if (non_sig == all_ns_cors or
                                    non_sig == all_ns_int or
                                    non_sig == list(set().union(all_ns_cors,
                                                                all_ns_int))):
                                    print("only correlation coefficients or intercepts are insignificant")
                                    return(sol, convergence)

                                if all([var in ps_asvars or var in ps_isvars or
                                        var in ps_rvars.keys() for var in non_sig]):
                                    print("non-significant terms are pre-specified")
                                    return(sol, convergence)

                                if (len([var for var in non_sig if var in
                                        ['sd.' + var for var
                                         in ps_rvars.keys()]]) == len(non_sig)):
                                    print("non-significant terms are pre-specified random coefficients")
                                    return(sol, convergence)

                            else:
                                # convergence = False
                                print("convergence not reached in round 2 so final sol is from round 1")
                                return(sol, convergence)
                        else:
                            print("no vars for round 2")
                            return(sol, convergence)
            else:
                convergence = False
                print("convergence not reached in round 1")
                return(sol, convergence)
        else:
            print("no vars when function called first time")
        return(sol, convergence)

    # Initialize harmony memory and opposite harmony memory of size HMS with random slutions
    def initialize_memory(self, choice_data, HMS, asvars_avail, isvars_avail,
                          rvars_avail, bcvars_avail, corvars_avail, asvars_ps,
                          isvars_ps, rvars_ps, bcvars_ps, corvars_ps,
                          bctrans_ps, cor_ps, intercept_ps, trans_asvars,
                          asvarnames, choice_set, alt_var, choice_var,
                          choice_id, ind_id, ps_asvars, isvarnames, ps_isvars,
                          ps_intercept, ps_rvars, ps_corvars):
        """
        Creates two lists (called the harmony memory and opposite harmony memory)
        harmony memory - containing the initial randomly generated solutions
        opposite harmony memory - containing random solutions that include variables not included in harmony memory
        Inputs: harmony memory size (int), all variable names, individual-specific variable, prespecifications provided by user
        """
        init_HM = self.code_name + 'initialize_memory_' + \
                  self.current_date + '.txt'
        if self.verbose < 2:
            sys.stdout = open(init_HM, 'wt')  # TODO: TURN OFF?

        # Set Random Seed  # TODO: INVESTIGATE
        global_seed = 1609
        np.random.seed(global_seed)
        seeds = np.random.choice(50000, 23000, replace=False)

        # HM_sol_labels = create_sol_labels(1,HM_size+1)
        # OHM_sol_labels = create_sol_labels(HMS+1,(HMS*2)+1)

        # set random seeds

        HM = []
        opp_HM = []
        base_model = [1000000, -1e+8, [], [], {}, [], [], False]  # TODO

        HM.append(base_model)
        # print("HM with base model is",HM)

        # Add an MXL with full covriance structure

        # Create initial harmony memory
        unique_HM = []
        for i in range(len(seeds)):
            seed = seeds[i]
            asvars, isvars, randvars, bcvars, corvars, bctrans, cor, \
            asconstant = \
                self.generate_sol(choice_data, self.df_test, seed, asvars_avail,
                                  isvars_avail, rvars_avail, trans_asvars,
                                  bcvars_avail, corvars_avail, asvars_ps,
                                  isvars_ps, rvars_ps, bcvars_ps,
                                  corvars_ps, bctrans_ps, cor_ps, intercept_ps,
                                  asvarnames, choice_set, alt_var)
            sol, conv = \
                self.evaluate_objective_function(choice_data, self.df_test, seed, asvars,
                                                 isvars, randvars, bcvars,
                                                 corvars, choice_var,
                                                 self.test_choice, alt_var,
                                                 choice_id, ind_id, asconstant,
                                                 ps_asvars, asvarnames,
                                                 isvarnames, ps_isvars,
                                                 ps_intercept, choice_set,
                                                 ps_rvars, ps_corvars)
            if conv:
                # add to memory
                # Similarity check to keep only unique solutions in harmony memory
                # TODO? CHECK STILL WANTED
                if len(HM) > 0:  # only do check if there are already solutions
                    bic_list = [hm_sol[0] for hm_sol in HM]
                    discrepancy = 0.1 * min(bic_list)  # TODO!: arbitrary!

                    unique_HM_discrepancy = []
                    for sol_hm in HM:
                        # TODO: below line makes no sense
                        if np.abs(sol_hm[0] - sol_hm[0]) <= discrepancy:
                            unique_HM_discrepancy.append(sol_hm)

                    if len(unique_HM_discrepancy) > 0:
                        # check if varnames, randvars, bcvars, corrvars and
                        # fit are the same as similar BIC solns
                        # if 2 or more are same then do not accept solution
                        # TODO! CHECK / IMPROVE INDICES...
                        hm_varnames = [sol_hm[2] for sol_hm in unique_HM_discrepancy]
                        hm_randnames = [sol_hm[4] for sol_hm in unique_HM_discrepancy]
                        hm_trans = [sol_hm[5] for sol_hm in unique_HM_discrepancy]
                        hm_correlation = [sol_hm[6] for sol_hm in unique_HM_discrepancy]
                        hm_intercept = [sol_hm[7] for sol_hm in unique_HM_discrepancy]

                        similarities = 0
                        if sol[2] in hm_varnames:
                            similarities += 1

                        if len(sol[4]) > 0 and sol[4] in hm_randnames:
                            similarities += 1

                        if len(sol[5]) > 0 and sol[5] in hm_trans:
                            similarities += 1

                        # if len(sol[6]) > 0 and sol[6] in hm_correlation:
                            # similarities += 1

                        if sol[7] in hm_intercept:
                            similarities += 1

                        if similarities > 3:  # accepts solution if 2 or more aspects of solution are different
                            conv = False  # make false so solution isn't added
            if conv:
                HM.append(sol)
                # keep only unique solutions in memory
                used = set()
                unique_HM = [used.add(tuple(x[:1])) or x for x in HM
                             if tuple(x[:1]) not in used]
                unique_HM = sorted(unique_HM, key=lambda x: x[0])
                print("harmony memory for iteration", i, "is", unique_HM)

            print("estimating opposite harmony memory")
            # if len(unique_HM) == HMS:

            # create opposite harmony memory with variables that were not included in the harmony memory's solution

            # list of variables that were not present in previously generated solution for HM
            ad_var = [x for x in self.varnames if x not in sol[2]]
            seed = seeds[i+HMS]
            op_asvars, op_isvars, op_rvars, op_bcvars, op_corvars, \
                op_bctrans, op_cor, op_asconstant = \
                    self.generate_sol(choice_data, self.df_test, seed,
                                      asvars_avail, isvars_avail,
                                      rvars_avail, trans_asvars, bcvars_avail,
                                      corvars_avail, asvars_ps, isvars_ps,
                                      rvars_ps,
                                      bcvars_ps, corvars_ps, bctrans_ps,
                                      cor_ps,
                                      intercept_ps, asvarnames, choice_set,
                                      alt_var)

            # evaluate objective function of opposite solution
            print("opp sol features", op_asvars, op_isvars, op_rvars,
                  op_bcvars, op_corvars, op_bctrans, op_cor, op_asconstant)
            opp_sol, opp_conv = \
                self.evaluate_objective_function(choice_data, self.df_test,
                                                 seed, op_asvars,
                                                 op_isvars, op_rvars,
                                                 op_bcvars, op_corvars,
                                                 choice_var,
                                                 self.test_choice,
                                                 alt_var,
                                                 choice_id, ind_id,
                                                 op_asconstant, ps_asvars,
                                                 asvarnames, isvarnames,
                                                 ps_isvars, ps_intercept,
                                                 choice_set, ps_rvars,
                                                 ps_corvars)
            if opp_conv:
                # Similarity check to keep only unique solutions in opposite harmony memory
                if len(opp_HM) > 0:  # only do check if there are already solutions
                    bic_list = [sol[0] for sol in self.unique_opp_HM]
                    discrepancy = 0.1 * min(bic_list)    # TODO: arbitrary choice ... improve?

                    unique_opp_HM_discrepancy = []
                    for opp in opp_HM:
                        if np.abs(opp[0] - opp_sol[0]) <= discrepancy:
                            unique_opp_HM_discrepancy.append(opp)

                    if len(unique_opp_HM_discrepancy) > 0:
                        # check if varnames, randvars, bcvars, corrvars and fit
                        # are the same as similar BIC solns
                        # if 2 or more are same then do not accept solution
                        opp_HM_varnames = [sol[2] for sol in unique_opp_HM_discrepancy]
                        opp_HM_randnames = [sol[4] for sol in unique_opp_HM_discrepancy]
                        opp_HM_trans = [sol[5] for sol in unique_opp_HM_discrepancy]
                        opp_HM_correlation = [sol[6] for sol in unique_opp_HM_discrepancy]
                        opp_HM_intercept = [sol[7] for sol in unique_opp_HM_discrepancy]

                        similarities = 0
                        if opp_sol[2] in opp_HM_varnames:
                            similarities += 1

                        if opp_sol[4] in opp_HM_randnames:
                            similarities += 1

                        if opp_sol[5] in opp_HM_trans:
                            similarities += 1

                        if opp_sol[6] in opp_HM_correlation:
                            similarities += 1

                        if opp_sol[7] in opp_HM_intercept:
                            similarities += 1

                        # accepts solution if 2 or more aspects of solution are different
                        if similarities > 3:
                            opp_conv = False  # make false so solution isn't added

            if opp_conv:
                opp_HM.append(opp_sol)
                opp_used = set()
                unique_opp_HM = [opp_used.add(tuple(x[:1])) or x for x in opp_HM
                                 if tuple(x[:1]) not in opp_used]
                unique_opp_HM = sorted(unique_opp_HM, key=lambda x: x[0])
                print("unique_opp_HM is for iteration", i, "is", unique_opp_HM)
                self.unique_opp_HM = unique_opp_HM  # TODO? POOR
                if len(unique_opp_HM) == HMS:
                        break

            # Final Initial Harmony
            Init_HM = unique_HM + unique_opp_HM
            unique = set()
            unique_Init_HM = [unique.add(tuple(x[:1])) or x for x in Init_HM
                              if tuple(x[:1]) not in unique]
            if len(unique_Init_HM) >= HMS:
                unique_Init_HM = unique_Init_HM[:HMS]
                return(unique_Init_HM)
                # break
        return(unique_Init_HM)
        # sys.stdout.flush()

        # return(unique_HM,unique_opp_HM)
    # We need to make sure that the BICs of solutions in harmony memory are different from each other by atleast the throshold value

    def harmony_consideration(self, har_mem, HMCR_itr, seeds, itr, HMS, df,
                              avail_asvars, avail_isvars, avail_rvars,
                              trans_asvars, avail_bcvars, avail_corvars,
                              ps_asvars, ps_isvars, ps_rvars, ps_bcvars,
                              ps_corvars, ps_bctrans, ps_cor, ps_intercept,
                              asvarnames, choice_set, alt_var, HM):
        """
        If a generated random number is less than or equal to the harmony memory consideration rate (HMCR)
        then 90% of a solution already in memory will be randomly selected to build the new solution.
        Else a completely new random solution is generated
        Inputs: harmony memory, HMCR for the current interation, random seeds, iteration number
        """
        seed = seeds[HMS*2+itr]
        new_sol = []
        har_mem = self.non_dominant_sorting(har_mem)
        Fronts = self.get_fronts(har_mem)
        Pareto = self.pareto(Fronts, har_mem)

        if np.random.choice([0, 1], p=[1-HMCR_itr, HMCR_itr]) <= HMCR_itr:
            print("harmony consideration")
            m_pos = np.random.choice(len(har_mem)) #randomly choose the position of any one solution in harmony memory
            select_new_asvars_index = np.random.choice([0, 1],
                                                       size=len(har_mem[m_pos][2]),
                                                       p=[1-HMCR_itr, HMCR_itr])
            select_new_asvars = [i for (i, v) in zip(har_mem[m_pos][2],
                                                     select_new_asvars_index)
                                                     if v]
            select_new_asvars = list(np.random.choice(har_mem[m_pos][2],
                                                      int((len(har_mem[m_pos][2]))*HMCR_itr),
                                                      replace=False))  # randomly select 90% of the variables from solution at position m_pos in harmony memory
            n_asvars = sorted(list(set().union(select_new_asvars, ps_asvars)))
            new_asvars = self.remove_redundant_asvars(n_asvars, trans_asvars,
                                                      seed, asvarnames)
            new_sol.append(new_asvars)
            print("new_asvars", new_asvars)

            select_new_isvars_index = np.random.choice([0, 1],
                                                       size=len(har_mem[m_pos][3]),
                                                       p=[1-HMCR_itr, HMCR_itr])
            select_new_isvars = [i for (i, v) in zip(har_mem[m_pos][3], select_new_isvars_index) if v]
            # select_new_isvars = list(np.random.choice(har_mem[m_pos][2],int((len(har_mem[m_pos][2]))*HMCR_itr),replace = False, p=[1-HMCR_itr, HMCR_itr]))
            new_isvars = sorted(list(set().union(select_new_isvars, ps_isvars)))
            print("new_isvars", new_isvars)
            new_sol.append(new_isvars)

            # include distributions for the variables in new solution based on the solution at m_pos in memory
            # TODO: RYAN ADD - SAFEGUARD
            if m_pos < len(Pareto):
                r_pos = {k: v for k, v in har_mem[m_pos][4].items() if k
                         in new_asvars}
                print("r_pos", r_pos)
                new_sol.append(r_pos)
            else:
                new_sol.append(dict())

            new_bcvars = [var for var in har_mem[m_pos][5] if var in new_asvars
                          and var not in ps_corvars]
            new_sol.append(new_bcvars)

            new_corvars = [var for var in har_mem[m_pos][6] if var
                           in r_pos.keys() and var not in new_bcvars]
            new_sol.append(new_corvars)

            # Take fit_intercept from m_pos solution in memory
            intercept = har_mem[m_pos][7]
            new_sol.append(intercept)
            print("new sol after HMC-1", new_sol)
        else:
            print("harmony not considered")
            # if harmony memory consideration is not conducted, then a new solution is generated

            asvars, isvars, randvars, bcvars, corvars, bctrans, cor, asconstant = \
                self.generate_sol(df, self.df_test, seed, avail_asvars,
                                  avail_isvars, avail_rvars, trans_asvars,
                                  avail_bcvars, avail_corvars, ps_asvars,
                                  ps_isvars, ps_rvars, ps_bcvars,
                                  ps_corvars, ps_bctrans, ps_cor,
                                  ps_intercept, asvarnames, choice_set,
                                  alt_var)
            new_sol = [asvars, isvars, randvars, bcvars, corvars, asconstant]  # TODO? RYAN ADD IN VAL
            print("new sol after HMC-2", new_sol)
        return(new_sol)

    def add_new_asfeature(self, solution, seed):
        """
        Randomly selects an as variable, which is not already in solution
        Inputs: solution list contianing all features generated from harmony consideration
        ##TODO: Include alternative-specific coefficients
        """
        new_asvar = [var for var in self.asvarnames if var not in solution[0]]
        print('new_asvar', new_asvar)
        if new_asvar:
            n_asvar = list(np.random.choice(new_asvar, 1))
            solution[0].extend(n_asvar)
            solution[0] = self.remove_redundant_asvars(solution[0],
                                                       self.trans_asvars,
                                                       seed,
                                                       self.asvarnames)
            solution[0] = sorted(list(set(solution[0])))
            print("new sol", solution[0])

            dis = []
            r_vars = {}
            for i in solution[0]:
                if i in solution[2].keys():
                    r_vars.update({k: v for k, v in solution[2].items()
                                   if k == i})
                    print("r_vars", r_vars)
                else:
                    if i in self.ps_rvars.keys():
                        r_vars.update({i: self.ps_rvars[i]})
                        print("r_vars", r_vars)
                    else:
                        if len(self.dist) > 0:  # TODO: RYAN ADD
                            r_vars.update({i: np.random.choice(self.dist)})
                        print("r_vars", r_vars)
            solution[2] = {k: v for k, v in r_vars.items() if k
                           in solution[0] and v != 'f'}

        solution[4] = [var for var in solution[4] if var in solution[2].keys()
                       and var not in solution[3]]
        # TODO: is this the right solution indices? does it switch up throughout?
        if self.ps_intercept is None:
            solution[5] = bool(np.random.randint(2))
        print(solution)
        return(solution)

    def add_new_isfeature(self, solution):
        """
        Randomly selects an is variable, which is not already in solution
        Inputs: solution list contianing all features generated from harmony consideration
        """
        if solution[1]:
            new_isvar = [var for var in self.isvarnames if var
                         not in solution[1]]
            if new_isvar:
                n_isvar = list(np.random.choice(new_isvar, 1))
                solution[1] = sorted(list(set(solution[1]).union(n_isvar)))
        return(solution)

    def add_new_bcfeature(self, solution, PAR_itr):
        """
        Randomly selects a variable to be transformed, which is not already in solution
        Inputs: solution list contianing all features generated from harmony consideration
        """
        if self.ps_bctrans is None:
            bctrans = bool(np.random.randint(2, size=1))
        else:
            bctrans = self.ps_bctrans
        if bctrans:
            select_new_bcvars_index = np.random.choice([0, 1],
                                                       size=len(solution[0]),
                                                       p=[1-PAR_itr, PAR_itr])
            new_bcvar = [i for (i, v) in zip(solution[0],
                                             select_new_bcvars_index) if v]
            solution[3] = sorted(list(set(solution[3]).union(new_bcvar)))
            solution[3] = [var for var in solution[3] if var
                           not in self.ps_corvars]
        else:
            solution[3] = []
        solution[4] = [var for var in solution[4] if var not in solution[3]]
        return(solution)

    def add_new_corfeature(self, solution):
        """
        Randomly selects variables to be correlated, which is not already in solution
        Inputs: solution list contianing all features generated from harmony consideration
        """
        if self.ps_cor is None:
            cor = bool(np.random.randint(2, size=1))
        else:
            cor = self.ps_cor
        if cor:
            new_corvar = [var for var in solution[2].keys() if var
                          not in solution[3]]
            solution[4] = sorted(list(set(solution[4]).union(new_corvar)))
        else:
            solution[4] = []
        if len(solution[4]) < 2:
            solution[4] = []
        solution[3] = [var for var in solution[3] if var not in solution[4]]
        return(solution)

    def remove_asfeature(self, solution):
        """
        Randomly excludes an as variable from solution generated from harmony consideration
        Inputs: solution list contianing all features
        """
        if solution[0]:
            rem_asvar = list(np.random.choice(solution[0], 1))
            solution[0] = [var for var in solution[0] if var not in rem_asvar]
            solution[0] = sorted(list(set(solution[0]).union(self.ps_asvars)))
            solution[2] = {k: v for k, v in solution[2].items() if k
                           in solution[0]}
            solution[3] = [var for var in solution[3] if var in solution[0]
                           and var not in self.ps_corvars]
            solution[4] = [var for var in solution[4] if var in solution[0]
                           and var not in self.ps_bcvars]
        return(solution)

    def remove_isfeature(self, solution):
        """
        Randomly excludes an is variable from solution generated from harmony consideration
        Inputs: solution list contianing all features
        """
        if solution[1]:
            rem_isvar = list(np.random.choice(solution[1], 1))
            solution[1] = [var for var in solution[1] if var not in rem_isvar]
            solution[1] = sorted(list(set(solution[1]).union(self.ps_isvars)))
        return(solution)

    def remove_bcfeature(self, solution):
        """
        Randomly excludes a variable transformation from solution generated from harmony consideration
        Inputs: solution list contianing all features
        """
        if solution[3]:
            rem_bcvar = list(np.random.choice(solution[3], 1))
            rem_nps_bcvar = [var for var in rem_bcvar if var
                             not in self.ps_bcvars]
            solution[3] = [var for var in solution[3] if var in solution[0]
                           and var not in rem_nps_bcvar]
            solution[4] = [var for var in solution[4] if var not in solution[3]]
            solution[3] = [var for var in solution[3] if var not in solution[4]]
        return(solution)

    def remove_corfeature(self, solution):
        """
        Randomly excludes correlaion feature from solution generated from harmony consideration
        Inputs: solution list contianing all features
        """
        if solution[4]:
            rem_corvar = list(np.random.choice(solution[4], 1))
            rem_nps_corvar = [var for var in rem_corvar if var
                              not in self.ps_corvars]
            solution[4] = [var for var in solution[4] if var
                           in solution[2].keys() and var not in rem_nps_corvar]
            if len(solution[4]) < 2:
                solution[4] = []
        return(solution)

    def assess_sol(self, solution, har_mem, seed):
        """
        (1) Evaluates the objective function of a given solution
        (2) Evaluates if the solution provides an improvement in BIC by atleast a threshold value compared to any other solution in memory
        (3) Checks if the solution is unique to other solutions in memory
        (4) Replaces the worst solution in memory, if (2) and (3) are true
        Inputs: solution list contianing all features, harmony memory
        """
        data = self.df.copy()
        improved_sol, conv = \
            self.evaluate_objective_function(data, self.df_test, seed,
                                             solution[0], solution[1],
                                             solution[2], solution[3],
                                             solution[4], self.choice_var,
                                             self.test_choice, self.alt_var,
                                             self.choice_id, self.ind_id,
                                             solution[5], self.ps_asvars,
                                             self.asvarnames, self.isvarnames,
                                             self.ps_isvars, self.ps_intercept,
                                             self.choice_set, self.ps_rvars,
                                             self.ps_corvars)
        if conv:
            har_mem.append(improved_sol)
            # TODO? what happened to below
            # if all(har_mem[sol][0] != improved_sol[0] for sol in range(len(har_mem))):
            #     if all(har_mem[sol][0] - improved_sol[0] >= threshold for sol in range(1,len(har_mem))):
            #         if all(abs(har_mem[sol][0]-improved_sol[0]) >= threshold for sol in range(len(har_mem))):
            #             har_mem[-1] = improved_sol
        seen = set()
        seen_add = seen.add
        new_hm = [x for x in har_mem if tuple(x[:2]) not in seen and
                  not seen_add(tuple(x[:2]))]

        fronts = self.get_fronts(new_hm)
        Pareto = self.pareto(fronts, new_hm)
        new_har_mem = self.non_dominant_sorting(new_hm)
        print("new_har_mem", new_har_mem)
        return(new_har_mem, improved_sol)

    def pitch_adjustment(self, sol, har_mem, PAR_itr, seeds, itr, HMS):
        seed = seeds[HMS*3+itr]
        """
        (1) A random binary indicator is generated. If the number is 1,
            then a new feature is added to the solution
            generated in the Harmony Memory consideration step.
            Else a feature is randomly excluded from the solution
        (2) The objective function of a given solution is evaluated.
        (3) The worst solution in harmony memory is repalced with the solution,
            if it is unique and provides an improved BIC

        Inputs:
        solution list generated from harmony consideration step
        harmony memory
        Pitch adjustment rate for the given iteration
        """
        improved_harmony = har_mem
        if np.random.choice([0, 1], p=[1-PAR_itr, PAR_itr]) <= PAR_itr:
            if np.random.randint(2):
                print("pitch adjustment adding as variables")
                pa_sol = self.add_new_asfeature(sol, seed)
                improved_harmony, current_sol = self.assess_sol(pa_sol,
                                                                har_mem,
                                                                seed)

                if self.isvarnames:
                    print("pitch adjustment adding is variables")
                    pa_sol = self.add_new_isfeature(pa_sol)
                    improved_harmony, current_sol = self.assess_sol(pa_sol,
                                                                    har_mem,
                                                                    seed)

                if self.ps_bctrans is None or self.ps_bctrans:
                    print("pitch adjustment adding bc variables")
                    pa_sol = self.add_new_bcfeature(pa_sol, PAR_itr)
                    improved_harmony, current_sol = self.assess_sol(pa_sol,
                                                                    har_mem,
                                                                    seed)

                if self.ps_cor is None or self.ps_cor:
                    print("pitch adjustment adding cor variables")
                    pa_sol = self.add_new_corfeature(pa_sol)
                    improved_harmony, current_sol = self.assess_sol(pa_sol,
                                                                    har_mem,
                                                                    seed)

            elif len(sol[0]) > 1:
                print("pitch adjustment by removing as variables")
                pa_sol = self.remove_asfeature(sol)
                improved_harmony, current_sol = self.assess_sol(pa_sol,
                                                                har_mem,
                                                                seed)

                if self.isvarnames or sol[1]:
                    print("pitch adjustment by removing is variables")
                    pa_sol = self.remove_isfeature(pa_sol)
                    improved_harmony, current_sol = self.assess_sol(pa_sol,
                                                                    har_mem,
                                                                    seed)

                if self.ps_bctrans is None or self.ps_bctrans:
                    print("pitch adjustment by removing bc variables")
                    pa_sol = self.remove_bcfeature(pa_sol)
                    improved_harmony, current_sol = self.assess_sol(pa_sol,
                                                                    har_mem,
                                                                    seed)

                if self.ps_cor is None or self.ps_cor:
                    print("pitch adjustment by removing cor variables")
                    pa_sol = self.remove_corfeature(pa_sol)
                    improved_harmony, current_sol = self.assess_sol(pa_sol,
                                                                    har_mem,
                                                                    seed)
            else:
                print("pitch adjustment by adding asfeature")
                pa_sol = self.add_new_asfeature(sol, seed)
                improved_harmony, current_sol = self.assess_sol(pa_sol,
                                                                har_mem,
                                                                seed)
        else:
            print("no pitch adjustment")
            improved_harmony, current_sol = self.assess_sol(sol, har_mem, seed)
        return(improved_harmony, current_sol)

    def best_features(self, har_mem):
        """
        Generates lists of best features in harmony memory
        Inputs:
        Harmony memory
        """
        HM = self.find_bestsol(har_mem)
        best_asvars = HM[2].copy()
        best_isvars = HM[3].copy()
        best_randvars = HM[4].copy()
        best_bcvars = HM[5].copy()
        best_corvars = HM[6].copy()
        asc_ind = HM[7]
        return(best_asvars, best_isvars, best_randvars, best_bcvars,
               best_corvars, asc_ind)

    def local_search(self, improved_harmony, seeds, itr, PAR_itr):
        """
        Initiate Artificial Bee-colony optimization
        Check if finetuning the best solution in harmony improves solution's BIC
        Inputs: improved memory after harmony consideration and pitch adjustment
        """
        seed = seeds[self.HMS*4+itr]
        # For plots (BIC vs. iterations)
        best_bic_points = []
        current_bic_points = []
        x = []
        # pp = PdfPages('BIC_plots_localsearch.pdf')

        # Select best solution features
        best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, \
            asc_ind = self.best_features(improved_harmony)

        print("first set of best features input for local search",
              best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars)
        # for each additional feature to the best solution, the objective function is tested

        # Check if changing coefficient distributions of best solution improves the solution BIC
        for var in best_randvars.keys():
            if var not in self.ps_rvars:
                rm_dist = [dis for dis in self.dist if dis != best_randvars[var]]
                best_randvars[var] = np.random.choice(rm_dist)
        best_randvars = {key: val for key, val in best_randvars.items()
                         if key in best_asvars and val != 'f'}
        best_bcvars = [var for var in best_bcvars if var in best_asvars
                       and var not in self.ps_corvars]
        best_corvars = [var for var in best_randvars.keys() if var
                        not in best_bcvars]
        solution_1 = [best_asvars, best_isvars, best_randvars, best_bcvars,
                      best_corvars, asc_ind]
        print(solution_1)
        improved_harmony, current_sol = self.assess_sol(solution_1,
                                                        improved_harmony,
                                                        seed)
        print("sol after local search step 1", improved_harmony[0])

        # check if having a full covariance matrix has an improvement in BIC
        best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, \
            asc_ind = self.best_features(improved_harmony)
        best_bcvars = [var for var in best_asvars if var in self.ps_bcvars]
        if self.ps_cor is None or self.ps_cor:
            best_corvars = [var for var in best_randvars.keys() if var
                            not in best_bcvars]
        elif len(best_corvars) < 2:
            best_corvars = []
        else:
            best_corvars = []
        solution_2 = [best_asvars, best_isvars, best_randvars, best_bcvars,
                      best_corvars, asc_ind]
        improved_harmony, current_sol = self.assess_sol(solution_2,
                                                        improved_harmony,
                                                        seed)
        print("sol after local search step 2", improved_harmony[0])

        # check if having a all the variables transformed has an improvement in BIC
        best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, \
            asc_ind = self.best_features(improved_harmony)
        if self.ps_bctrans is None or self.ps_bctrans:
            best_bcvars = [var for var in best_asvars if var
                           not in self.ps_corvars]
        else:
            best_bcvars = []
        best_corvars = [var for var in best_randvars.keys() if var
                        not in best_bcvars]
        solution_3 = [best_asvars, best_isvars, best_randvars, best_bcvars,
                      best_corvars, asc_ind]
        improved_harmony, current_sol = self.assess_sol(solution_3,
                                                        improved_harmony,
                                                        seed)
        print("sol after local search step 3", improved_harmony[0])

        if len(best_asvars) < len(self.asvarnames):
            print("local search by adding variables")
            solution = [best_asvars, best_isvars, best_randvars, best_bcvars,
                        best_corvars, asc_ind]
            solution_4 = self.add_new_asfeature(solution, seed)
            improved_harmony, current_sol = self.assess_sol(solution_4,
                                                            improved_harmony,
                                                            seed)
            print("sol after local search step 4", improved_harmony[0])

        best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, \
            asc_ind = self.best_features(improved_harmony)
        solution = [best_asvars, best_isvars, best_randvars, best_bcvars,
                    best_corvars, asc_ind]
        solution_5 = self.add_new_isfeature(solution)
        improved_harmony, current_sol = self.assess_sol(solution_5,
                                                        improved_harmony,
                                                        seed)
        print("sol after local search step 5", improved_harmony[0])

        best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, \
             asc_ind = self.best_features(improved_harmony)
        solution = [best_asvars, best_isvars, best_randvars, best_bcvars,
                    best_corvars, asc_ind]
        solution_6 = self.add_new_bcfeature(solution, PAR_itr)
        improved_harmony, current_sol = self.assess_sol(solution_6,
                                                        improved_harmony,
                                                        seed)
        print("sol after local search step 6", improved_harmony[0])

        best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, \
            asc_ind = self.best_features(improved_harmony)
        solution = [best_asvars, best_isvars, best_randvars, best_bcvars,
                    best_corvars, asc_ind]
        solution_7 = self.add_new_corfeature(solution)
        improved_harmony, current_sol = self.assess_sol(solution_7,
                                                        improved_harmony,
                                                        seed)
        print("sol after local search step 7", improved_harmony[0])

        # Sort unique harmony memory from min.BIC to max. BIC
        # improved_harmony = sorted(improved_harmony, key = lambda x: x[0])

        # Check if changing coefficient distributions of best solution improves the solution BIC
        best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, \
            asc_ind = self.best_features(improved_harmony)

        for var in best_randvars.keys():
            if var not in self.ps_rvars:
                rm_dist = [dis for dis in self.dist if dis != best_randvars[var]]
                best_randvars[var] = np.random.choice(rm_dist)
        best_randvars = {key: val for key, val in best_randvars.items()
                         if key in best_asvars and val != 'f'}
        best_bcvars = [var for var in best_bcvars if var in best_asvars and
                       var not in self.ps_corvars]
        if self.ps_cor is None or self.ps_cor:
            best_corvars = [var for var in best_randvars.keys() if var
                            not in best_bcvars]
        if self.ps_cor is False:
            best_corvars = []
        if len(best_corvars) < 2:
            best_corvars = []
        solution = [best_asvars, best_isvars, best_randvars, best_bcvars,
                    best_corvars, asc_ind]
        improved_harmony, current_sol = self.assess_sol(solution,
                                                        improved_harmony,
                                                        seed)
        print("sol after local search step 8", improved_harmony[0])

        # check if having a full covariance matrix has an improvement in BIC
        best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, \
            asc_ind = self.best_features(improved_harmony)
        best_bcvars = [var for var in best_asvars if var in self.ps_bcvars]
        if self.ps_cor is None or self.ps_cor:
            best_corvars = [var for var in best_randvars.keys() if var not in best_bcvars]
        else:
            best_corvars = []
        if len(best_corvars) < 2:
            best_corvars = []
        solution = [best_asvars, best_isvars, best_randvars, best_bcvars,
                    best_corvars, asc_ind]
        improved_harmony, current_sol = self.assess_sol(solution, improved_harmony,
                                                        seed)
        print("sol after local search step 9", improved_harmony[0])

        # check if having all the variables transformed has an improvement in BIC
        best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, \
            asc_ind = self.best_features(improved_harmony)
        if self.ps_bctrans is None or self.ps_bctrans:
            best_bcvars = [var for var in best_asvars if var not in self.ps_corvars]
        else:
            best_bcvars = []
        if self.ps_cor is None or self.ps_cor:
            best_corvars = [var for var in best_randvars.keys()
                            if var not in best_bcvars]
        else:
            best_corvars = []

        if len(best_corvars) < 2:
            best_corvars = []
        solution = [best_asvars, best_isvars, best_randvars, best_bcvars,
                    best_corvars, asc_ind]
        improved_harmony, current_sol = self.assess_sol(solution,
                                                        improved_harmony,
                                                        seed)
        print("sol after local search step 10", improved_harmony[0])

        # Sort unique harmony memory from min.BIC to max. BIC
        # final_harmony_sorted = sorted(improved_harmony, key = lambda x: x[0])
        final_harmony_sorted = improved_harmony
        return(final_harmony_sorted, current_sol)

        # TODO? OLD CODE BELOW -- CONFIRM AND REMOVE
        # if all variables in varnames are present in the best solution, we improvise the solution by changing some features
        # if len(best_asvars) == len(self.asvarnames):
        #     ##Check if changing coefficient distributions of best solution improves the solution BIC
        #     for var in best_randvars.keys():
        #         if var not in self.ps_rvars:
        #             rm_dist = [dis for dis in self.dist if dis != best_randvars[var]]
        #             best_randvars[var] = np.random.choice(rm_dist)
        #     best_randvars = {key:val for key,val in best_randvars.items() if key in best_asvars and val != 'f'}
        #     best_bcvars = [var for var in best_bcvars if var in best_asvars and var not in self.ps_corvars]
        #     best_corvars = [var for var in best_randvars.keys() if var not in best_bcvars]
        #     solution_1 = [best_asvars, best_isvars,best_randvars,best_bcvars,best_corvars,asc_ind]
        #     improved_harmony, current_sol = self.assess_sol(solution_1,improved_harmony,seed)
        #     print("sol after local search step 1", improved_harmony[0])

        #     ##check if having a full covariance matrix has an improvement in BIC
        #     best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, asc_ind = best_features(improved_harmony)
        #     best_bcvars = [var for var in best_asvars if var in self.ps_bcvars]
        #     if self.ps_cor == None or self.ps_cor == True:
        #         best_corvars = [var for var in best_randvars.keys() if var not in best_bcvars]
        #     elif len(best_corvars)<2:
        #         best_corvars = []
        #     else:
        #         best_corvars = []
        #     solution_2 = [best_asvars, best_isvars,best_randvars,best_bcvars,best_corvars,asc_ind]
        #     improved_harmony, current_sol = self.assess_sol(solution_2,improved_harmony,seed)
        #     print("sol after local search step 2", improved_harmony[0])

        #     # check if having a all the variables transformed has an improvement in BIC
        #     best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, asc_ind = best_features(improved_harmony)
        #     if self.ps_bctrans == None or self.ps_bctrans == True:
        #         best_bcvars = [var for var in best_asvars if var not in self.ps_corvars]
        #     else:
        #         best_bcvars = []
        #     best_corvars = [var for var in best_randvars.keys() if var not in best_bcvars]
        #     solution_3 = [best_asvars, best_isvars,best_randvars,best_bcvars,best_corvars,asc_ind]
        #     improved_harmony, current_sol = self.assess_sol(solution_3,improved_harmony,seed)
        #     print("sol after local search step 3", improved_harmony[0])
        # else:
        #     print("local search by adding variables")
        #     solution = [best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, asc_ind]
        #     solution_4 = self.add_new_asfeature(solution,seed)
        #     improved_harmony, current_sol = self.assess_sol(solution_4,\
        #     improved_harmony,seed)
        #     print("sol after local search step 4", improved_harmony[0])

        #     best_asvars, best_isvars, best_randvars, best_bcvars,\
        #     best_corvars, asc_ind = self.best_features(improved_harmony)
        #     solution = [best_asvars, best_isvars, best_randvars, \
        #     best_bcvars, best_corvars, asc_ind]
        #     solution_5 = self.add_new_isfeature(solution)
        #     improved_harmony, current_sol = self.assess_sol(solution_5, \
        #     improved_harmony,seed)
        #     print("sol after local search step 5", improved_harmony[0])

        #     best_asvars, best_isvars, best_randvars, best_bcvars, \
        #     best_corvars, asc_ind = self.best_features(improved_harmony)
        #     solution = [best_asvars, best_isvars, best_randvars, best_bcvars,\
        #     best_corvars, asc_ind]
        #     solution_6 = self.add_new_bcfeature(solution)
        #     improved_harmony, current_sol = self.assess_sol(solution_6,improved_harmony,seed)
        #     print("sol after local search step 6", improved_harmony[0])

        #     best_asvars, best_isvars, best_randvars, best_bcvars, \
        #     best_corvars, asc_ind = self.best_features(improved_harmony)
        #     solution = [best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, asc_ind]
        #     solution_7 = self.add_new_corfeature(solution)
        #     improved_harmony, current_sol = self.assess_sol(solution_7,improved_harmony,seed)
        #     print("sol after local search step 7", improved_harmony[0])

        # # Sort unique harmony memory from min.BIC to max. BIC
        # improved_harmony = sorted(improved_harmony, key = lambda x: x[0])

        # # Check if changing coefficient distributions of best solution improves the solution BIC
        # best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, \
        # asc_ind = self.best_features(improved_harmony)

        # for var in best_randvars.keys():
        #     if var not in ps_rvars:
        #         rm_dist = [dis for dis in self.dist if dis != best_randvars[var]]
        #         best_randvars[var] = np.random.choice(rm_dist)
        # best_randvars = {key:val for key, val in best_randvars.items() if key in best_asvars and val != 'f'}
        # best_bcvars = [var for var in best_bcvars if var in best_asvars and var not in self.ps_corvars]
        # if self.ps_cor == None or self.ps_cor == True:
        #     best_corvars = [var for var in best_randvars.keys() if var not in best_bcvars]
        # elif self.ps_cor == False:
        #     best_corvars = []
        # if len(best_corvars)<2:
        #     best_corvars = []
        # solution = [best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, asc_ind]
        # improved_harmony, current_sol = self.assess_sol(solution,improved_harmony,seed)
        # print("sol after local search step 8", improved_harmony[0])

        # check if having a full covariance matrix has an improvement in BIC
        # best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, \
        #  asc_ind = self.best_features(improved_harmony)
        # best_bcvars = [var for var in best_asvars if var in self.ps_bcvars]
        # if self.ps_cor == None or self.ps_cor == True:
        #     best_corvars = [var for var in best_randvars.keys() if var not in best_bcvars]
        # else:
        #     best_corvars = []
        # if len(best_corvars)<2:
        #     best_corvars = []
        # solution = [best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, asc_ind]
        # improved_harmony, current_sol = self.assess_sol(solution,improved_harmony,seed)
        # print("sol after local search step 9", improved_harmony[0])

        # ##check if having all the variables transformed has an improvement in BIC
        # best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, \
        # asc_ind = self.best_features(improved_harmony)
        # if self.ps_bctrans == None or self.ps_bctrans == True:
        #     best_bcvars = [var for var in best_asvars if var not in ps_corvars]
        # else:
        #     best_bcvars = []
        # if self.ps_cor == None or self.ps_cor == True:
        #     best_corvars = [var for var in best_randvars.keys() if var not in best_bcvars]
        # else:
        #     best_corvars = []
        # if len(best_corvars)<2:
        #     best_corvars = []
        # solution = [best_asvars, best_isvars, best_randvars, best_bcvars, best_corvars, asc_ind]
        # improved_harmony, current_sol = self.assess_sol(solution,improved_harmony,seed)
        # print("sol after local search step 10", improved_harmony[0])

        # Sort unique harmony memory from min.BIC to max. BIC
        # final_harmony_sorted = sorted(improved_harmony, key = lambda x: x[0])
        # return(final_harmony_sorted,current_sol)

    # Function to conduct harmony memory consideraion, pitch adjustment and local search
    def improvise_harmony(self, HCR_max, HCR_min, PR_max, PR_min, har_mem,
                          max_itr, threshold, itr_prop,
                          ps_corvars, ps_bctrans, ps_cor, ps_intercept,
                          asvarnames, choice_set, alt_var, HM):
        # Set Random Seed  # TODO: INVESTIGATE
        global_seed = 1609
        np.random.seed(global_seed)
        seeds = np.random.choice(50000, 23000, replace=False)

        improve_harmony = self.code_name + 'improvise_harmony_' + self.current_date + '.txt'
        sys.stdout = open(improve_harmony, 'wt')
        itr = 0

        # for BIC vs. iteration plots
        best_bic_points = []
        current_bic_points = []
        best_val_points = []
        # pdf_name = 'BIC_plots_final_' + self.code_name + self.current_date + '.pdf'
        # pp = PdfPages(pdf_name)
        # np.random.seed(500)
        np.random.seed(seeds[itr])
        while itr < max_itr:
            itr += 1
            # print(itr)
            # Estimate dynamic HMCR and PCR values for each iteration
            HMCR_itr = (HCR_min + ((HCR_max-HCR_min)/max_itr)*itr) * max(0, math.sin(itr))
            PAR_itr = (PR_min + ((PR_max-PR_min)/max_itr)*itr) * max(0, math.sin(itr))
            # seed = seeds[itr]
            # Conduct Harmony Memory Consideration
            hmc_sol = \
                self.harmony_consideration(har_mem, HMCR_itr, seeds, itr, self.HMS,
                                           self.df, self.avail_asvars, self.avail_isvars,
                                           self.avail_rvars, self.trans_asvars,
                                           self.avail_bcvars, self.avail_corvars,
                                           self.ps_asvars, self.ps_isvars, self.ps_rvars,
                                           self.ps_bcvars,
                                           ps_corvars, ps_bctrans, ps_cor,
                                           ps_intercept, asvarnames,
                                           choice_set, alt_var, HM)
            print("solution after HMC at iteration", itr, "is", hmc_sol)
            # Conduct Pitch Adjustment
            pa_hm, current_sol = self.pitch_adjustment(hmc_sol, har_mem,
                                                       PAR_itr, seeds, itr,
                                                       self.HMS)
            print("best solution after HMC & PA at iteration", itr, "is", pa_hm[0])
            current_bic_points.append(current_sol[0])
            # Sort unique harmony memory from min.BIC to max. BIC
            # har_mem_sorted = sorted(pa_hm, key = lambda x: x[0])
            har_mem = pa_hm
            # Trim the Harmony memory's size as per the harmony memory size
            # har_mem = har_mem_sorted[:HMS]
            # Append y-axis points for the plots
            best_bic_points = [har_mem[x][0] for x in range(len(har_mem))]
            best_val_points = [har_mem[x][1] for x in range(len(har_mem))]
            print(best_bic_points, best_val_points)
            # plt.scatter(best_val_points, best_bic_points)
            # plt.xlabel('Validation measure')
            # plt.ylabel('BIC')
            # plt.plot(best_val_points, best_bic_points, label="Pareto solutions")
            sys.stdout.flush()
            # plt.show()
            sys.stdout.flush()

            # check iteration to initiate local search
            if itr > int(itr_prop * max_itr):
                print("HM before starting local search", har_mem)
                print("local search initiated at iteration", itr)
                # seed = seeds[itr]
                har_mem, current_sol = self.local_search(har_mem, seeds, itr,
                                                         PAR_itr)
                # Sort unique harmony memory from min.BIC to max. BIC
                # har_mem = sorted(har_mem, key = lambda x: x[0])
                # Trim the Harmony memory's size as per the harmony memory size
                # har_mem = har_mem[:HMS]

                print("final harmony in current iteration", itr, "is", har_mem)

                best_bic_points.append(har_mem[0][0])
                current_bic_points.append(current_sol[0])
                print(har_mem[0][0])
                # x.append(itr)
                best_bic_points = [har_mem[x][0] for x in range(len(har_mem))]
                best_val_points = [har_mem[x][1] for x in range(len(har_mem))]
                print(har_mem[0][0])

                # plt.scatter(best_val_points, best_bic_points)
                # plt.xlabel('Validation measure')
                # plt.ylabel('BIC')
                # pp.savefig(plt.gcf())
                # plt.show()
                sys.stdout.flush()
            sys.stdout.flush()

            if itr == max_itr+1:
                break
                """
                #plt.figure()
                #plt.xlabel('Iterations')
                #plt.ylabel('BIC')
                #plt.plot(x, current_bic_points, label = "BIC from current iteration")
                plt.plot(x, best_bic_points, label = "BIC of best solution in memory")
                #pp.savefig(plt.gcf())
                plt.show()
                """

        # pp.close()  # TODO: IF OPENED?
        # plt.plot(x, best_bic_points, label = "BIC of best solution in memory")
        # plt.savefig("best_bic_points.png")
        sys.stdout.flush()
        return(har_mem, best_bic_points, current_bic_points)

    def _prep_inputs(self, asvarnames=[], isvarnames=[]):
        """Include modellers' model prerequisites if any."""
        # pre-included alternative-sepcific variables
        # binary indicators representing alternative-specific variables
        # that are prespecified by the user
        psasvar_ind = [0] * len(asvarnames)

        # binary indicators representing individual-specific variables prespecified by the user
        psisvar_ind = [0] * len(isvarnames)

        # pre-included distributions
        # pspecdist_ind = ["f"]* 9 + ["any"] * (len(asvarnames)-9)
        # variables whose coefficient distribution have been prespecified by the modeller
        pspecdist_ind = ["any"] * len(asvarnames)

        # prespecification on estimation of intercept
        ps_intercept = None  # (True or False or None)

        # prespecification on transformations
        ps_bctrans = False  # (True or False or None)
        # indicators representing variables with prespecified transformation by the modeller
        ps_bcvar_ind = [0] * len(asvarnames)

        # prespecification on estimation of correlation
        ps_cor = False  # (True or False or None)
        # [1,1,1,1,1] indicators representing variables with prespecified correlation by the modeller
        ps_corvar_ind = [0] * len(asvarnames)

        # prespecified interactions
        ps_interaction = None  # (True or False or None)  # TODO? REMOVE?
        return (psasvar_ind, psisvar_ind, pspecdist_ind, ps_bcvar_ind,
                ps_corvar_ind)

    def run_search(self, HMS=10):
        psasvar_ind, psisvar_ind, pspecdist_ind, ps_bcvar_ind, ps_corvar_ind = \
            self._prep_inputs(asvarnames=self.asvarnames, isvarnames=self.isvarnames)
        ps_bctrans = False  # (True or False or None)  # TODO
        ps_cor = False  # (True or False or None) # TODO
        ps_interaction = None  # (True or False or None) # TODO
        ps_intercept = None  # (True or False or None)

        ps_asvars, ps_isvars, ps_rvars, ps_bcvars, ps_corvars = \
            self.prespec_features(psasvar_ind, psisvar_ind, pspecdist_ind,
                                  ps_bcvar_ind, ps_corvar_ind, self.isvarnames,
                                  self.asvarnames)
        self.ps_asvars = ps_asvars
        self.ps_isvars = ps_isvars
        self.ps_intercept = ps_intercept
        self.ps_rvars = ps_rvars
        self.ps_corvars = ps_corvars
        self.ps_bctrans = ps_bctrans
        self.ps_cor = ps_cor
        self.ps_bcvars = ps_bcvars
        self.ps_interaction = ps_interaction
        avail_asvars, avail_isvars, avail_rvars, avail_bcvars, avail_corvars = \
            self.avail_features(ps_asvars, ps_isvars, ps_rvars, ps_bcvars,
                                ps_corvars, self.isvarnames, self.asvarnames)
        # TODO: SAVING AVAILS HERE TO STOP BUG
        self.avail_asvars = avail_asvars
        self.avail_isvars = avail_isvars

        # TODO! 
        avail_rvars = []
        self.avail_rvars = avail_rvars
        self.avail_bcvars = avail_bcvars
        self.avail_corvars = avail_corvars
        # TODO? 5 is a random seed?
        asvars_new = self.df_coeff_col(5,
                                       self.df,
                                       self.df_test,
                                       avail_asvars,
                                       self.choice_set,
                                       self.alt_var)
        self.remove_redundant_asvars(asvars_new, self.trans_asvars, 3,
                                     self.asvarnames)
        self.generate_sol(self.df, self.df_test, 2, avail_asvars, avail_isvars,
                          avail_rvars, self.trans_asvars, avail_bcvars,
                          avail_corvars, ps_asvars, ps_isvars, ps_rvars,
                          ps_bcvars, ps_corvars, ps_bctrans, ps_cor,
                          ps_intercept, self.asvarnames, self.choice_set,
                          self.alt_var)
        Init_HM = self.initialize_memory(self.df, HMS, avail_asvars,
                                         avail_isvars, avail_rvars,
                                         avail_bcvars, avail_corvars,
                                         ps_asvars, ps_isvars, ps_rvars,
                                         ps_bcvars, ps_corvars, ps_bctrans,
                                         ps_cor, ps_intercept,
                                         self.trans_asvars, self.asvarnames,
                                         self.choice_set, self.alt_var,
                                         self.choice_var, self.choice_id,
                                         self.ind_id, ps_asvars,
                                         self.isvarnames, ps_isvars,
                                         ps_intercept, ps_rvars, ps_corvars)
        # Combine both harmonies
        # Init_HM = HM + O_HM

        # Remove duplicate solutions if present
        unique = set()
        unique_HM = [unique.add(tuple(x[:1])) or x for x in Init_HM if tuple(x[:1]) not in unique]

        # Sort unique harmony memory from min.BIC to max. BIC
        HM_sorted = sorted(unique_HM, key=lambda x: x[0])

        # Trim the Harmony memory's size as per the harmony memory size
        HM = HM_sorted[:HMS]
        hm = HM.copy()

        # TODO! IMPORTANT TUNING PARAMS HERE
        self.HMS = HMS
        HMCR_min = 0.6  # 0.9 #minimum harmony memory consideration rate
        HMCR_max = 0.9  # 0.99 #maximum harmony memory consideration rate
        PAR_max = 0.85
        PAR_min = 0.3  # 0.8 #min pitch adjustment
        itr_max = 30  # TODO?
        # proportion of iterations to improvise harmony. The rest will be for local search
        v = 0.80
        threshold = 15  # threshold to compare new solution with worst solution in memory
        self.val_share = 0.25  # TODO? MAKE ALL TUNING PARAMS SELF ATTRIBUTES?

        Initial_harmony = hm.copy()
        new_HM, best_BICs, current_BICs = \
            self.improvise_harmony(HMCR_max, HMCR_min, PAR_max, PAR_min,
            Initial_harmony, itr_max,
            threshold, v,
            # HMS, self.df, avail_asvars,
            # avail_isvars, avail_rvars, self.trans_asvars, avail_bcvars,
            # avail_corvars, ps_asvars, ps_isvars, ps_rvars, ps_bcvars,
            ps_corvars, ps_bctrans, ps_cor, ps_intercept, self.asvarnames,
            self.choice_set, self.alt_var, HM)
        improved_harmony = new_HM.copy()

        # benchmark_bic = improved_harmony[0][0]  # TODO? not used
        # best_asvarnames = improved_harmony[0][1]
        # best_isvarnames = improved_harmony[0][2]
        # best_randvars = improved_harmony[0][3]
        # best_bcvars = improved_harmony[0][4]
        # best_corvars = improved_harmony[0][5]
        # best_Intercept = improved_harmony[0][6]
        # benchmark_bic,best_asvarnames,best_isvarnames,best_randvars,best_bcvars,best_corvars,best_Intercept
        # TODO! SOOF VS MOOF ??

        if self.multi_objective:
            # TODO!
            hm = self.non_dominant_sorting(improved_harmony)
            best_sol = hm[0]
        else:  # single objective - bic, the 0-th index
            improved_harmony.sort(key=lambda x: x[0], reverse=True)
            best_sol = improved_harmony[0]
        print("Search ended at", time.ctime())
        benchmark_bic = best_sol[0]  # TODO? not used
        benchmark_val = best_sol[1]
        best_asvarnames = best_sol[2]
        best_isvarnames = best_sol[3]
        best_randvars = best_sol[4]
        best_bcvars = best_sol[5]
        best_corvars = best_sol[6]
        best_Intercept = best_sol[7]

        best_varnames = best_asvarnames + best_isvarnames
        df = self.df
        if bool(best_randvars):
            if self.latent_class:
                model = LatentClassMixedModel()
                # TODO! FIX THIS UP WHEN INCORPORATE CLASS PARAMS
                model.fit(X, y, varnames=best_varnames, isvars=best_isvarnames,
                          #   class_params_spec=class_params_spec,  # TODO!
                          #   member_params_spec=member_params_spec, # TODO!
                          num_classes=self.num_classes, alts=self.alt_var,
                          ids=id_choice, panels=self.ind_id,
                          fit_intercept=best_Intercept,
                          transformation="boxcox", transvars=best_bcvars,
                          randvars=best_randvars,
                          correlation=best_corvars,
                          maxiter=self.maxiter, gtol=self.gtol,
                          avail=self.avail,
                          weights=self.weights)
            else:
                model = MixedLogit()
                model.fit(X=df[best_varnames], y=self.choice_var, varnames=best_varnames,
                        isvars=best_isvarnames, alts=self.alt_var, ids=self.choice_id,
                        panels=self.ind_id, randvars=best_randvars,
                        transformation="boxcox", transvars=best_bcvars,
                        correlation=best_corvars, fit_intercept=best_Intercept,
                        n_draws=200)
        else:
            if self.latent_class:
                model = LatentClassModel()
                # TODO! FIX THIS UP WHEN INCORPORATE CLASS PARAMS
                model.fit(X, y, varnames=best_varnames, isvars=best_isvarnames,
                          #   class_params_spec=class_params_spec,  # TODO!
                          #   member_params_spec=member_params_spec, # TODO!
                          num_classes=self.num_classes, alts=self.alt_var,
                          ids=id_choice, fit_intercept=best_Intercept,
                          transformation="boxcox", transvars=best_bcvars,
                        #   randvars=best_randvars,
                        #   correlation=best_corvars,
                          maxiter=self.maxiter, gtol=self.gtol, avail=self.avail,
                          weights=self.weights)
            else:
                model = MultinomialLogit()
                model.fit(X=df[best_varnames], y=self.choice_var,
                        varnames=best_varnames, isvars=best_isvarnames,
                        alts=self.alt_var, ids=self.choice_id,
                        transformation="boxcox", transvars=best_bcvars,
                        fit_intercept=best_Intercept)
        print(model.summary())
        print(best_BICs)
        print(current_BICs)
        sys.stdout.flush()  # TODO?

    def check_dominance(self, obj1, obj2):
        """
        Function checks dominance between solutions for two objective functions
        Inputs: obj1 - List containing values of the two objective functions for solution 1
                obj2 - List containing values of the two objective functions for solution 2
        Output: Returns True if solution 1 dominates 2, False otherwise
        """
        indicator = False
        for a, b in zip(obj1, obj2):
            if a < b:
                indicator = True
            # if one of the objectives is dominated, then return False
            elif a > b:
                return False
        return indicator

    # Final Pareto-front identifier
    def get_fronts(self, HM):
        """
        Funtion for non-dominant sorting of the given set of solutions
        ni - the number of solutions which dominate the solution i
        si - a set of solutions which the solution i dominates

        Inputs: List containing set of solutions

        Output: Dict with keys indicating the Pareto rank and values containing indices of solutions in Input
        """
        si = {}
        ni = {}
        for i in range(len(HM)):
            sp_i = []
            np_i = 0
            for j in range(len(HM)):
                if i != j:
                    dominance = self.check_dominance(HM[i][:2], HM[j][:2])
                    if dominance:
                        # print("sol" + " " + str(i) + " " + "dominates" + " " + "sol" + " " + str(j))
                        sp_i.append(j)
                    else:
                        dominance = self.check_dominance(HM[j][:2], HM[i][:2])
                        if dominance:
                            # print("sol" + " " + str(i) + " " + "does not dominate" + " " + "sol" + " " + str(j))
                            np_i += 1
            si.update({i: sp_i})
            ni.update({i: np_i})
        # print(ni,si)
        # Identify solutions in each front
        Fronts = {}
        itr = 0
        for k in range(max(ni.keys())):
            Fi_idx = [key for key, val in ni.items() if val == k]
            if len(Fi_idx) > 0:
                Fronts.update({'F_{}'.format(itr): Fi_idx})
                itr += 1
        print("Fronts", Fronts)
        return(Fronts)

    def crowding_dist(self, Fronts, HM):
        """
        Function to estimate crowding distance between 2 solutions
        Inputs:
        Fronts-Dict with keys indicating Pareto rank and values indicating indices of solutions belonging to the rank
        HM - List of solutions
        """
        v_dis = {}
        for v in Fronts.values():
            v.sort(key=lambda x: HM[x][0])
            for i in v:
                v_dis.update({i: 0})
        # Calculate crowding distance based on first objective
        for v in Fronts.values():
            for j in v:
                if v[0] == j or v[-1] == j:
                    v_dis.update({j: 1000000})
                else:
                    dis = abs(v_dis.get(j) +
                              ((HM[v[v.index(j) + 1]][0] -
                                HM[j][0]) / (max(HM[x][0] for x in
                                                 range(len(HM))) -
                                             min(HM[x][0] for x in
                                                 range(len(HM))))))
                    v_dis.update({j: dis})

        # Calculate crowding distance based on second objective
        q_dis = {}
        for v in Fronts.values():
            v.sort(key=lambda x: HM[x][1])
            for k in v:
                q_dis.update({k: 0})
        for v in Fronts.values():
            for l in v:
                if v[0] == l or v[-1] == l:
                    q_dis.update({l: 1000000})
                else:
                    dis = abs(q_dis.get(l) + ((HM[v[v.index(l)+1]][1] -
                                               HM[l][1])
                                               / (max(HM[x][1] for x
                                                     in range(len(HM))) -
                                                 min(HM[x][1] for x in
                                                     range(len(HM))))))
                    q_dis.update({l: dis})
        # Adding crowding distance from both objectives
        crowd = {k: q_dis[k] + v_dis[k] for k in v_dis.keys()}
        return(crowd)

    def pareto(self, Fronts, HM):
        Pareto_front_id = []
        for k, v in Fronts.items():
            if len(v) > 0:
                Pareto_front_id = Fronts.get(k)
                break
        Pareto_front = [HM[x] for x in Pareto_front_id]
        return(Pareto_front)
    # Fronts = get_fronts(unique_HM)
    # pareto_front = pareto(Fronts,unique_HM)
    # pareto_front

    def sort_InitHM(self, Fronts, v_dis, HM):
        """
        Function to sort memory from best solution to worst solution
        Inputs:
        Fronts-Dict with keys indicating Pareto rank and values indicating indices of solutions belonging to the rank
        v_dis - Dict with keys indicating index of solution in memory and value indicating crowding distance
        Output:
        Sorted_HM - Sorted list of solutions
        """
        Sorted_HM_id = []
        for k, v in Fronts.items():
            pareto_sols = {key: val for key, val in v_dis.items() if key
                            in Fronts.get(k)}
            Sorted_HM_id.extend([ke for ke, va in
                                sorted(pareto_sols.items(),
                                       key=lambda item: item[1],
                                       reverse=True)])
            # print(Sorted_HM_id)
            # Sorted_HM_id.extend([ke for ke, va in sorted(pareto_sols.items(), key=lambda item: item[1])])
            if len(Sorted_HM_id) >= self.HMS:
                break
        Sorted_HM = [HM[x] for x in Sorted_HM_id]
        return(Sorted_HM)

    def non_dominant_sorting_initHM(self, HM):
        Front = self.get_fronts(HM)
        crowd = self.crowding_dist(Front, HM)
        Final_HM = self.sort_InitHM(Front, crowd, HM)
        return(Final_HM)

    # hm = non_dominant_sorting_initHM(unique_HM)
    # print("Final Initial Harmony", hm)
    # fronts = get_fronts(hm)
    # pf = pareto(fronts,hm)
    # print("Initial Front", pf)

    def sort_HM(self, Fronts, v_dis, HM):
        """
        Function to sort memory from best solution to worst solution
        Inputs:
        Fronts-Dict with keys indicating Pareto rank and values indicating indices of solutions belonging to the rank
        v_dis - Dict with keys indicating index of solution in memory and value indicating crowding distance
        Output:
        Sorted_HM - Sorted list of solutions
        """
        Sorted_HM_id = []
        for k, v in Fronts.items():
            pareto_sols = {key: val for key, val in v_dis.items()
                           if key in Fronts.get(k)}
            # Sorted_HM_id.extend([ke for ke, va in sorted(pareto_sols.items(), key=lambda item: item[1], reverse = True)])
            Sorted_HM_id.extend([ke for ke, va in
                                 sorted(pareto_sols.items(),
                                        key=lambda item: item[1])])
            # if len(Sorted_HM_id) >= HMS:
            # break
        Sorted_HM = [HM[x] for x in Sorted_HM_id]
        return(Sorted_HM)

    def non_dominant_sorting(self, HM):
        Front = self.get_fronts(HM)
        crowd = self.crowding_dist(Front, HM)
        Final_HM = self.sort_HM(Front, crowd, HM)
        return(Final_HM)

    def find_bestsol(self, HM):
        max_obj1 = max(HM[x][0] for x in range(len(HM)))
        max_obj2 = max(HM[x][1] for x in range(len(HM)))
        min_obj1 = min(HM[x][0] for x in range(len(HM)))
        min_obj2 = min(HM[x][1] for x in range(len(HM)))
        weights_obj1 = [(HM[x][0])-min_obj1/(max_obj1-min_obj1) for x in range(len(HM))]
        weights_obj2 = [(HM[x][1])-min_obj2/(max_obj2-min_obj2) for x in range(len(HM))]
        weights = [weights_obj1[x] + weights_obj2[x] for x in range(len(HM))]
        best_solid = weights.index(min(weights))
        print("best sol for local search", HM[best_solid])
        return(HM[best_solid])
