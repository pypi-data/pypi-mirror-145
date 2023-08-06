# import numpy as np
#
# from gym import Space
#
# class ObservationSpaceDAO(Space):
#     max_ratio = 3.0
#
#     def __init__(self):
#         super(ObservationSpaceDAO, self).__init__()
#
#     def sample(self):
#         return np.random.uniform(0, ObservationSpaceDAO.max_ratio, 4)
#
#     def contains(self, obs, x):
#         return len(obs) == 4 and (obs >= 0.0).all() and (x <= ObservationSpaceDAO.max_ratio).all()
#
#     def to_jsonable(self, sample_n):
#         return np.array(sample_n).to_list()
#
#     def from_jsonable(self, sample_n):
#         return [np.asarray(sample) for sample in sample_n]
#
#
# class ObservationSpaceTrader(Space):
#     max_ratio = 3.0
#
#     def __init__(self):
#         super(ObservationSpaceTrader, self).__init__()
#
#     def sample(self):
#         return np.random.uniform(0, ObservationSpaceTrader.max_ratio, 4)
#
#     def contains(self, obs, x):
#         return len(obs) == 4 and (obs >= 0.0).all() and (x <= ObservationSpaceTrader.max_ratio).all()
#
#     def to_jsonable(self, sample_n):
#         return np.array(sample_n).to_list()
#
#     def from_jsonable(self, sample_n):
#         return [np.asarray(sample) for sample in sample_n]
#
#
# class ObservationSpaceArbitrageur(Space):
#     max_ratio = 3.0
#
#     def __init__(self):
#         super(ObservationSpaceArbitrageur, self).__init__()
#
#     def sample(self):
#         return np.random.uniform(0, ObservationSpaceArbitrageur.max_ratio, 4)
#
#     def contains(self, obs, x):
#         return len(obs) == 4 and (obs >= 0.0).all() and (x <= ObservationSpaceArbitrageur.max_ratio).all()
#
#     def to_jsonable(self, sample_n):
#         return np.array(sample_n).to_list()
#
#     def from_jsonable(self, sample_n):
#         return [np.asarray(sample) for sample in sample_n]
#
#
# observation_space = {
#     'DAO': ObservationSpaceDAO,
#     'Trader': ObservationSpaceTrader,
#     'Arbitrageur': ObservationSpaceArbitrageur
# }