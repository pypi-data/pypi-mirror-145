import csv
import pandas as pd
import numpy as np
import os
import networkx as nx
from multiprocessing import Pool, cpu_count


class Pedigree:
    """
    Pedigree class is based on the old format, a DataFrame with the variables:

    _id_ unique id individual
    _f_  0 if there is no father
    _m_  0 if there is no mother
    _proband 1 for proband and 0 for others
    _age_ current age
    _gender_ 1=male, 2=female, 9=unknown
    _ageOnsetBC1_ of the first breast cancer (0 if there is no breast cancer)
    _ageOnsetBC2_ of the second breast cancer (0 if there is no 2nd breast cancer)
    _ageOnsetPA_  of pancreatic cancer (0 if there is no 2nd breast cancer)
    _ageOnsetPR_  of prostate cancer (0 if there is no 2nd breast cancer)
    _ageOnsetOC_  of ovarian cancer (0 if there is no ovarian cancer)
    _genotype_  0 non-carrier, 1 carrier and 2 for unknown genotypes


    Methods:
        - founders
        - parents
        - enum_conf_p
        - enum_geno_p
        - enum_geno_p_par
        - enum_conf
        - enum_geno
        - enum_geno_par
        - enum_conf_pg
        - enum_geno_par_pg

    """

    def __init__(self, pedigree: pd.DataFrame = None, pedigree_path=None):
        """
        :param ped: pedigree
        """
        if pedigree_path is not None:
            self.ped = self.pedfile(pedigree_path)
        else:
            self.ped = pedigree
        self.ped.set_index(self.ped['id'].to_numpy(), inplace=True)
        self.ps = None
        self.gs = None

    def toid(self, x):
        return self.ped[x].index.to_list()

    @staticmethod
    def pedfile(file_path):
        """

        :param file_path:
        :return:
        """
        with open(file_path, 'rb') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.readline().decode('utf-8'))
            df = pd.read_csv(file_path, sep=dialect.delimiter)
            df.sort_values(by='id', inplace=True)
        return df

    def proband(self):
        return self.ped[self.ped.proband == 1].index.to_list()[0]

    def founders(self):
        """
        It tests whether both parents of 'id' are 0.
        :return: list of 1-based ids of founders
        """
        return self.toid(self.ped.apply(lambda x: x['f']+x['m'] == 0, axis=1))

    def parents_old(self, id):
        # _id = id - 1
        _id = id
        return [tuple(self.ped['f'])[_id], tuple(self.ped['m'])[_id]]

    def parents(self, id):
        """

        :param id: 1-based index
        :return:
        """
        if id in self.founders():
            return None
        else:
            return [self.ped['f'][id], self.ped['m'][id]]

    def ancestors(self, id):
        """
        :param id: zero-based id
        :return:
        """
        def anc(par):
            if par is None:
                return []
            else:
                return par + anc(self.parents(par[0])) + anc(self.parents(par[1]))
        return np.array(list(set(anc(self.parents(id)))))

    def offsprings(self, id):
        """

        :param id:
        :return:
        """
        return list(set(self.toid(self.ped['f'] == id) + self.toid(self.ped['m'] == id)))

    def descendants(self, id):
        """
        :param id:
        :return:
        """
        def dsc(id_):
            if len(self.offsprings(id_)) == 0:
                return []
            else:
                return [[i] + dsc(i) for i in self.offsprings(id_)]

        return self.flatten(dsc(id))

    def flatten(self, x):
        """
        :param x: a nested list without empty lists.
        :return: a flat list containing all element from the nested list.
        """
        if type(x) is list and len(x) > 1:
            (h, *t) = x
            if type(h) is list:
                return self.flatten(h) + self.flatten(t)
            else:
                return [h] + self.flatten(t)
        elif type(x) is list and len(x) == 1:
            return self.flatten(x[0])
        elif type(x) is list and len(x) == 0:
            return []
        else:
            return [x]

    def non_founders(self):
        return list(set(self.ped.index) - set(self.founders()))

    def graph(self):
        parent_child_rel = self.ped.loc[self.non_founders()][['id', 'm', 'f']]
        parent_child_edges = parent_child_rel.melt(id_vars=['id'])[['id', 'value']].to_records(index=False)
        spouse_edges = self.ped[self.ped.m !=0][['m', 'f']].drop_duplicates().to_records(index=False)
        edges = list(parent_child_edges) + list(spouse_edges)
        g = nx.Graph()
        g.add_edges_from(edges)
        return g

    def shortest_path(self, i, j):
        return np.array(list(set(nx.shortest_path(self.graph(), i, j))))

    def reachable_founders(self, id):
        return list(set(self.ancestors(id)).intersection(set(self.founders())))

    def observed(self):
        return self.ped.genotype!=2

    def n(self, observed=False):
        if not observed:
            return len(self.ped)
        else:
            return sum(self.observed())

    def configurations(self):

        def M():
            def mm_(founder_):
                mm = pd.Series(np.zeros(self.n()+1), dtype=int)  # take +1 larger vector
                sp = self.shortest_path(self.proband(), founder_)
                dc = self.descendants(founder_)
                mm.loc[sp] = 1
                mm.loc[list(set(dc).difference(set([self.proband()]).union(set(sp))))] = -1
                return mm[1:]  # remove index 0

            return [mm_(founder) for founder in self.reachable_founders(self.proband())]

        def H(x):
            def parents_known_genotype(i):
                parents_ = self.parents(i)
                if parents_ is None:
                    return False
                else:
                    return not (x[parents_]<0).any()
            # 1)
            hh = pd.Series([2 if (parents_known_genotype(i) & (v < 0)) else v for i, v in x.items()],index=x.index)
            # 2)
            while hh.isin([-1]).any():
                for i in hh.index:
                    if hh[i]<0:
                        parents_ = self.parents(i)
                        if parents_ is not None:
                            max_ = max(hh[parents_])
                            if max_ > 1:
                                hh[i] = max_ + 1

            return hh

        return [H(s) for s in M()]


    """ =================================================================
    OBSOLETE    
    ================================================================= """

    # def enum_conf_p(self, x):
    #     """
    #     :param x: is a list of integers, representing the generations
    #     :return:
    #     """
    #     if max(x) > 1:
    #
    #         # find index minimum above 1
    #         # gen = min([i for i in x if i > 1])
    #         # i = [idx for idx, v in enumerate(x) if v == gen][0]  # i=0..9
    #
    #         i = x[x > 1].index[0]
    #
    #         # pairs = [x[idx - 1] for idx in self.parents(i)]
    #         # cond = sum(pairs)
    #         parents_ = self.parents(i)
    #         if parents_ is not None:
    #             cond = sum(x[parents_])
    #         else:
    #             cond = 0
    #
    #         if cond == 0:
    #             x[i] = 0
    #             return self.enum_conf_p(x)
    #         elif cond == 1:
    #             x0 = x.copy()
    #             x0[i] = 0
    #             x1 = x.copy()
    #             x1[i] = 1
    #             return self.enum_conf_p(x1) + self.enum_conf_p(x0)
    #     else:
    #         pp = [self.parents(i) for i in x.index]
    #         return [sum([sum(x[p]) if p[0] != 0 else 0 for p in pp])]
    #
    # def enum_geno_p(self, confs):
    #     return [pow(0.5, v) for l in [self.enum_conf_p(conf) for conf in confs] for v in l]
    #
    # def enum_geno_p_par(self, confs, nodes=4):
    #     with Pool(nodes) as p:
    #         return [pow(0.5, v) for l in p.map(self.enum_conf_p, confs) for v in l]
    #
    # def enum_conf(self, x):
    #     """
    #     :param x: is a list of integers, representing the generations
    #     :return:
    #     """
    #     if max(x) > 1:
    #         # find index minimum above 1
    #         i = x[x > 1].index[0]
    #         parents_ = self.parents(i)
    #         if parents_ is not None:
    #             cond = sum(x[parents_])
    #         else:
    #             cond = 0
    #
    #         if cond == 0:
    #             x[i] = 0
    #             return self.enum_conf(x)
    #         elif cond == 1:
    #             x0 = x.copy()
    #             x0[i] = 0
    #             x1 = x.copy()
    #             x1[i] = 1
    #             return self.enum_conf(x1) + self.enum_conf(x0)
    #         else:
    #             raise Exception("Rare mutation assumption is not met for id " + str(i) + " !")
    #     else:
    #         return [x]
    #
    # def enum_geno(self, confs):
    #     """
    #     Generate all possibilities. enum_geno_par is the parallel version using Pool.
    #
    #     :param confs:
    #     :return:
    #     """
    #     return pd.concat([pd.DataFrame(self.enum_conf(conf)) for conf in confs], ignore_index=True)
    #
    # def enum_geno_par(self, confs):
    #     with Pool(4) as p:
    #         return pd.concat([pd.DataFrame(l) for l in p.map(self.enum_conf, confs)], ignore_index=True)
    #
    # def enum_conf_pg(self, x):
    #     """
    #     :param x: is a list of integers, representing the generations
    #     :return:
    #     """
    #
    #     if max(x) > 1:
    #         # find index minimum above 1
    #         gen = min([i for i in x if i > 1])
    #         i = [idx for idx, v in enumerate(x) if v == gen][0]  # i=0..9
    #         pairs = [x[idx - 1] for idx in self.parents_old(i)]  # idx range : 1..n, therefore idx-1 for pos in x
    #         cond = sum(pairs)  # sum(x[ped$parents(i)])
    #
    #         # i = x[x > 1].index[0]
    #         # parents_ = self.parents(i)
    #         # if parents_ is not None:
    #         #     cond = sum(x[parents_])
    #         # else:
    #         #     cond = 0
    #
    #         if cond == 0:
    #             x[i] = 0
    #             return self.enum_conf_pg(x)
    #         elif cond == 1:
    #             x0 = x.copy()
    #             x0[i] = 0
    #             x1 = x.copy()
    #             x1[i] = 1
    #             return self.enum_conf_pg(x1) + self.enum_conf_pg(x0)
    #         else:
    #             raise Exception("Rare mutation assumption is not met for id " + str(i) + " !")
    #     else:
    #         p_ = sum([x[p[0] - 1] + x[p[1] - 1] if p[0] != 0 else 0
    #                   for p in [self.parents_old(i) for i in range(0, len(x))]])
    #         return [(p_, [x])]
    #
    # def enum_geno_par_pg(self, confs):
    #     """
    #     _pg stands for combined p and genotype. The current p and genotype are almost identical except
    #     :param confs:
    #     :return:
    #     """
    #     with Pool(4) as p:
    #         gens_ = [g for g in p.map(self.enum_conf_pg, confs)]
    #     self.ps = [pow(0.5, p_) for c in gens_ for (p_, [x]) in c]
    #     self.gs = pd.DataFrame([x for c in gens_ for (p, [x]) in c])


    """ =================================================================
    enum_geno_par_pg and enum_conf_pg
    x => (p,x)    
    ================================================================= """

    def enum_conf_pg(self, x):
        """
        :param x: is a list of integers, representing the generations
        :return:
        """

        if max(x) > 1:
            # find index minimum above 1

            i = x[x > 1].index[0]
            parents_ = self.parents(i)
            if parents_ is not None:
                cond = sum(x[parents_])
            else:
                cond = 0

            if cond == 0:
                x[i] = 0
                return self.enum_conf_pg(x)
            elif cond == 1:
                x0 = x.copy()
                x0[i] = 0
                x1 = x.copy()
                x1[i] = 1
                return self.enum_conf_pg(x1) + self.enum_conf_pg(x0)
            else:
                raise Exception("Rare mutation assumption is not met for id " + str(i) + " !")
        else:
            pp = [self.parents(i) for i in x.index]
            p_ = sum([x[p[0]] + x[p[1]] if p is not None else 0 for p in pp])
            return [(p_, [x])]

    def enum_geno_par_pg(self):
        """
        _pg stands for combined p and genotype. The current p and genotype are almost identical except
        :return:
        """

        confs = self.configurations()
        if os.name == 'posix':
            with Pool(cpu_count()) as p:
                gens_ = [g for g in p.map(self.enum_conf_pg, confs)]
        else:
            gens_ = [self.enum_conf_pg(conf) for conf in confs]
        self.ps = [pow(0.5, p_) for c in gens_ for (p_, [x]) in c]
        self.gs = pd.DataFrame([x for c in gens_ for (p, [x]) in c])