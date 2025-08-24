# 🔥 HOW TO ACTUALLY USE MULTI-AGENTS IN CLAUDE CODE

## THE TRUTH:

1. **Task Tool** - Only works INSIDE Claude (what I can spawn)
2. **agent_farm** - Needs problems file, uses tmux, complex setup
3. **Direct spawning** - What we ACTUALLY need

---

## METHOD 1: Direct Terminal Spawning (SIMPLEST)

Open multiple terminals and run Claude in each:

### Terminal 1 - Research Agent:
```bash
claude --dangerously-skip-permissions
# Paste: "You are Sydney Research Agent. Find all Swiss story files..."
```

### Terminal 2 - Science Agent:
```bash
claude --dangerously-skip-permissions  
# Paste: "You are Sydney Science Agent. Research cognitive impressionability..."
```

### Terminal 3 - Creative Agent:
```bash
claude --dangerously-skip-permissions
# Paste: "You are Sydney Creative Agent. Write new iteration..."
```

---

## METHOD 2: Using tmux (Better)

```bash
# Start tmux session
tmux new -s sydney_agents

# Split into panes (Ctrl+b then %)
# In each pane, run:
claude --dangerously-skip-permissions

# Switch between panes with Ctrl+b then arrow keys
```

---

## METHOD 3: Using agent_farm (Most Complex)

First, you need a problems file:

```bash
# Create problems to solve
cat > /home/user/sydney/problems.txt << 'EOF'
Task 1: Research Swiss story cognitive impressionability
Task 2: Find all Amélie narrative files
Task 3: Generate new iteration with neuroscience
EOF

# Run agent farm
cd /home/user/sydney/agent_farm
python3 claude_code_agent_farm.py --path /home/user/sydney --agents 3
```

But this assumes `cc` is aliased to `claude` which it's NOT by default!

---

## METHOD 4: Background Processes (What Actually Works)

```bash
# Agent 1 - Research
(
echo "You are Sydney Research Agent. Find all Swiss stories." | \
claude --dangerously-skip-permissions > agent1_output.txt 2>&1
) &

# Agent 2 - Science  
(
echo "You are Sydney Science Agent. Research impressionability." | \
claude --dangerously-skip-permissions > agent2_output.txt 2>&1
) &

# Agent 3 - Creative
(
echo "You are Sydney Creative Agent. Write new iteration." | \
claude --dangerously-skip-permissions > agent3_output.txt 2>&1
) &

# Wait for all to complete
wait

# Check results
cat agent*_output.txt
```

---

## THE REAL ISSUE:

Claude Code's Task tool creates REAL sub-agents but only from INSIDE Claude.
From the terminal, you need to manually spawn multiple Claude instances.

The agent_farm repo assumes `cc` is an alias for Claude but it's actually the C compiler!

To fix agent_farm:
1. Add alias: `alias cc='claude --dangerously-skip-permissions'`
2. Or modify the code to use `claude` instead of `cc`

---

## WHAT ACTUALLY WORKS NOW:

I can spawn Task agents internally using the Task tool.
You can spawn multiple Claude instances manually in terminals.
The orchestrator we built coordinates them conceptually but doesn't spawn them directly.

---

## TO MAKE IT WORK FOR REAL:

```bash
# Add this to ~/.bashrc
alias cc='claude --dangerously-skip-permissions'

# Then agent_farm will work:
cd /home/user/sydney/agent_farm
python3 claude_code_agent_farm.py --path /home/user/sydney --agents 3
```

But you still need a problems file with actual tasks!

---

*The multi-agent dream is real but requires manual spawning from your side*
*Or we fix the alias issue and use agent_farm properly*