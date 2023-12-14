from stable_baselines3 import PPO, DDPG

from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecNormalize
from stable_baselines3.ppo import MlpPolicy 
from stable_baselines3.ppo import CnnPolicy
from save_on_best_result_callback import SaveOnBestTrainingRewardCallback
from stable_baselines3.common.vec_env.subproc_vec_env import SubprocVecEnv
from stable_baselines3.common.env_checker import check_env
from env.simglucose_gym_env import T1DSimEnv, T1DSimDiffEnv, T1DSimHistoryEnv, T1DDiscreteSimEnv, T1DAdultSimEnv
from reward.custom_rewards import custom_reward, shaped_reward_around_normal_bg, \
    shaped_negative_reward_around_normal_bg, no_negativity
import torch as th
import warnings





def main():
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    warnings.simplefilter(action='ignore', category=FutureWarning)
    total_time_steps = 128
    save_folder = r"C:\Users\yanni\diabetes-RL-project\test\new_model\adult"
    checkpoint_callback = CheckpointCallback(save_freq=256, save_path=save_folder,
                                             name_prefix="rl_model2")

    vec_env_kwargs = {'start_method': 'spawn'}
    env_kwargs = {'reward_fun': no_negativity}
    env = make_vec_env(T1DAdultSimEnv, n_envs=10, vec_env_cls=SubprocVecEnv,
                       vec_env_kwargs=vec_env_kwargs, env_kwargs=env_kwargs)
    
    policy_kwargs = {
    'net_arch': dict(pi=[32, 32], vf=[32, 32])
}


    model = PPO(MlpPolicy, env, verbose=1,
                n_steps=total_time_steps, learning_rate=2e-5, ent_coef=0.01,policy_kwargs=policy_kwargs,seed=465,
                gamma=0.85, n_epochs=15)
    model.learn(total_timesteps=1000000, callback=[checkpoint_callback])
    model.save(save_folder)


if __name__ == "__main__":
    main()