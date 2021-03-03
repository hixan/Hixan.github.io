import numpy as np
from pathlib import Path

np.set_printoptions(precision=2)


# simulation inputs
simulation_count = 100000
lambdas = np.array([2, 3, 4, 5])
probabilities = 1 / np.array([3, 5, 7, 11])

# draw from exponential distribution for all desks
gaps = np.random.exponential(1/lambdas, (simulation_count, len(lambdas)))

# turn into timestamps
times = np.cumsum(gaps, axis=0)

# draw from each column according to distribution
pass_on = np.random.uniform(size=times.shape) < probabilities

# sanity check - are the correct probabilites demonstrated and the correct
# lambdas?
print('simulated probabilities:', p_e:= np.mean(pass_on, axis=0), 'expected:',
        probabilities, '\ndiff:', p_e - probabilities, end='\n\n')
print('simultated lambdas:', l_e := np.mean(gaps, axis=0), 'expected:',
        lambdas, '\ndiff:', l_e - lambdas, end='\n\n')

# concatenate arrays and remove unwanted
supervisor = np.sort(np.concatenate(times)[np.concatenate(pass_on)])

# remove any past the last entry of the shortest simulation (to ensure all
# streams run for the same amount of time)
supervisor = supervisor[supervisor < np.min(times[-1,:])]

# print the final estimate
print('the mean time between customers for the supervisor was',
        res := np.diff(supervisor).mean(), '\nThis is accurate to'
        f' {np.abs(res - 1155/2648)/1155*2648 * 100:.2f}%.')

# Bonus: save data for visualization
import json

data_size = 500  # number of samples to save
maxtime = supervisor[data_size]

save_path = (Path(__file__).parent / 'data' /
        'simple_probability_question_dat.json')

data_export = [
    {
        'probability': p,
        'lambda': l,
    # rounding saves a lot of disk space (important as it will be served)
        'times': np.round(t[t <= maxtime], 2).tolist()
    }
    for p, l, t in zip(
        probabilities.astype(float),
        lambdas.astype(float),
        times.T.astype(float)
    )
]

with save_path.open('w') as f:
    json.dump(data_export, f)

