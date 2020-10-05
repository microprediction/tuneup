from sigopt import Connection
import logging
try:
    from tuneup.sigopt_credentials_private import SIG_KEY, PROJECT
except ImportError:
    pass
import uuid


def sigopt_cube(objective, scale, n_trials, n_dim):
  """
  :param objective:   returns 1-tuple
  :param scale:       float   defines cubical domain
  :param n_trials:    int
  :return:
  """
  params = [ {'name':'u'+str(i),'type':'double', 'bounds': {'min': -scale, 'max': scale}} for i in range(n_dim) ]
  metrics = [{'name': 'slimy_moose', 'objective': 'minimize'}]
  conn = Connection(client_token=SIG_KEY)
  experiment = conn.experiments().create(name='exp_'+str(uuid.uuid4())[:6],
                                         parameters=params,
                                         metrics=metrics,
                                         observation_budget=n_trials,
                                         project=PROJECT)
  def _objective(assignments):
      u = [ assignments['u'+str(i)] for i in range(n_dim) ]
      return objective(u)[0]

  while experiment.progress.observation_count < experiment.observation_budget:
      suggestion = conn.experiments(experiment.id).suggestions().create()
      value = _objective(assignments=suggestion.assignments)
      conn.experiments(experiment.id).observations().create(
        suggestion=suggestion.id,
        value=value,
      )
      experiment = conn.experiments(experiment.id).fetch()

  all_best_assignments = conn.experiments(experiment.id).best_assignments().fetch()
  return all_best_assignments.data[0].value


if __name__=='__main__':
  from tuneup.ndimsingleobjectives.ndimboxobjectives import AN_OBJECTIVE
  objective, scale = AN_OBJECTIVE
  print(sigopt_cube(objective=objective,scale=scale,n_trials=2,n_dim=10))
