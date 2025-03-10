""" 
 ===================== 
 Demo: demo_agent_manager_save 
 =====================
"""
import numpy as np
from rlberry.envs.benchmarks.ball_exploration import PBall2D
from rlberry.agents.torch.ppo import PPOAgent
from rlberry.manager import AgentManager, plot_writer_data, evaluate_agents


if __name__ == "__main__":
    # --------------------------------
    # Define train and evaluation envs
    # --------------------------------
    train_env = (PBall2D, dict())
    eval_env = (PBall2D, dict())

    # -----------------------------
    # Parameters
    # -----------------------------
    N_EPISODES = 100
    GAMMA = 0.99
    HORIZON = 50
    BONUS_SCALE_FACTOR = 0.1
    MIN_DIST = 0.1

    params_ppo = {"gamma": GAMMA, "horizon": HORIZON, "learning_rate": 0.0003}

    eval_kwargs = dict(eval_horizon=HORIZON, n_simulations=20)

    # -------------------------------
    # Run AgentManager and save results
    # --------------------------------
    ppo_stats = AgentManager(
        PPOAgent,
        train_env,
        fit_budget=N_EPISODES,
        init_kwargs=params_ppo,
        eval_kwargs=eval_kwargs,
        n_fit=4,
        output_dir="dev/",
        parallelization="process",
    )
    ppo_stats.fit()  # fit the 4 agents
    ppo_stats_fname = ppo_stats.save()
    del ppo_stats

    # -------------------------------
    # Load and plot results
    # --------------------------------
    ppo_stats = AgentManager.load(ppo_stats_fname)

    # learning curves
    plot_writer_data(
        ppo_stats,
        tag="episode_rewards",
        preprocess_func=np.cumsum,
        title="Cumulative Rewards",
        show=False,
    )

    # compare final policies
    output = evaluate_agents([ppo_stats], n_simulations=15)
    print(output)
