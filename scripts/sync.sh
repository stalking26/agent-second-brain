#!/bin/bash
# Auto-sync vault to GitHub with conflict prevention
# Used by cron every 5 minutes

LOCKFILE="/tmp/agent-second-brain-sync.lock"
PROJECT_DIR="$HOME/projects/agent-second-brain"
LOG="/tmp/agent-second-brain-sync.log"

# Prevent concurrent runs
if [ -f "$LOCKFILE" ]; then
    # Check if lock is stale (older than 5 minutes)
    if [ "$(find "$LOCKFILE" -mmin +5 2>/dev/null)" ]; then
        rm -f "$LOCKFILE"
    else
        exit 0
    fi
fi
trap 'rm -f "$LOCKFILE"' EXIT
touch "$LOCKFILE"

cd "$PROJECT_DIR" || exit 1

# Check if there are changes to commit
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    # No local changes — just pull
    git pull --ff-only origin main >> "$LOG" 2>&1 || true
    exit 0
fi

# Stage and commit local changes
git add -A
git commit -m "Auto-sync" >> "$LOG" 2>&1 || exit 0

# Pull remote changes with merge (not rebase!) to avoid conflict hell
git pull --no-rebase --no-edit origin main >> "$LOG" 2>&1
PULL_STATUS=$?

if [ $PULL_STATUS -ne 0 ]; then
    # Merge conflict — auto-resolve by keeping both (ours for session logs)
    CONFLICTED=$(git diff --name-only --diff-filter=U 2>/dev/null)
    if [ -n "$CONFLICTED" ]; then
        echo "$(date): Resolving conflicts in: $CONFLICTED" >> "$LOG"
        for f in $CONFLICTED; do
            case "$f" in
                vault/.sessions/*)
                    # Session files: keep local version (has latest data)
                    git checkout --ours "$f"
                    ;;
                vault/дневник/*)
                    # Daily notes: keep local version (has latest entries)
                    git checkout --ours "$f"
                    ;;
                *)
                    # Other files: keep local version
                    git checkout --ours "$f"
                    ;;
            esac
            git add "$f"
        done
        git commit --no-edit >> "$LOG" 2>&1 || true
    else
        # Not a merge conflict, abort
        git merge --abort 2>/dev/null
        echo "$(date): Pull failed (non-conflict), skipping push" >> "$LOG"
        exit 1
    fi
fi

# Push
git push origin main >> "$LOG" 2>&1 || echo "$(date): Push failed" >> "$LOG"
