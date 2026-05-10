"""Modern reinforcement-learning helpers for chapter 22 notebooks."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd


def ensure_output_dir(path: str | Path = "../data/deep_reinforcement_learning") -> Path:
    output = Path(path); output.mkdir(parents=True, exist_ok=True); return output


def value_iteration(size: int = 4, gamma: float = 0.9, iterations: int = 80) -> pd.DataFrame:
    V = np.zeros((size, size)); goal=(size-1,size-1)
    actions=[(1,0),(-1,0),(0,1),(0,-1)]
    for _ in range(iterations):
        new=V.copy()
        for r in range(size):
            for c in range(size):
                if (r,c)==goal: continue
                vals=[]
                for dr,dc in actions:
                    nr,nc=np.clip(r+dr,0,size-1),np.clip(c+dc,0,size-1)
                    vals.append(-1+gamma*V[nr,nc])
                new[r,c]=max(vals)
        V=new
    return pd.DataFrame(V)


def q_learning(size: int = 4, episodes: int = 500, alpha: float = 0.2, gamma: float = 0.9, seed: int = 22) -> pd.DataFrame:
    rng=np.random.default_rng(seed); actions=[(1,0),(-1,0),(0,1),(0,-1)]; Q=np.zeros((size,size,len(actions))); goal=(size-1,size-1)
    for _ in range(episodes):
        r,c=0,0
        for _step in range(80):
            a=rng.integers(len(actions)) if rng.random()<0.2 else Q[r,c].argmax()
            dr,dc=actions[a]; nr,nc=np.clip(r+dr,0,size-1),np.clip(c+dc,0,size-1)
            reward=10 if (nr,nc)==goal else -1
            Q[r,c,a]+=alpha*(reward+gamma*Q[nr,nc].max()-Q[r,c,a])
            r,c=nr,nc
            if (r,c)==goal: break
    policy=Q.argmax(axis=2)
    return pd.DataFrame(policy)


def lunar_lander_fallback(seed: int = 222) -> pd.DataFrame:
    rng=np.random.default_rng(seed)
    rewards=np.cumsum(rng.normal(0.5,2,200))
    return pd.DataFrame({'episode':range(200),'cumulative_reward':rewards})


def trading_q_learning(periods: int = 500, seed: int = 223) -> pd.DataFrame:
    rng=np.random.default_rng(seed); returns=rng.normal(0.0002,0.01,periods); q=np.zeros((3,3)); position=1; rows=[]
    for t,r in enumerate(returns):
        state=0 if r<-.005 else 2 if r>.005 else 1
        action=q[state].argmax(); new_position=action-1; reward=new_position*r
        q[state,action]+=0.1*(reward+0.9*q[state].max()-q[state,action])
        position=new_position; rows.append({'t':t,'return':r,'position':position,'strategy_return':reward})
    out=pd.DataFrame(rows); out['equity_curve']=(1+out.strategy_return).cumprod(); return out
