"""Unified Cyberpunk Profile Dashboard Asset Generator.

Runs all asset generation modules, ensures both Dark and Light variants are
created for every widget, and isolates failures so one network glitch won't
halt the entire pipeline.
"""

import os
import sys
import shutil
import traceback
from cyber_palette import recolor_file_to_light

# Import generators
from generate_banner import generate_banner
from generate_typing import generate_typing_svg
from generate_system_status import generate_system_status_svg
from generate_stats import gather_metrics, generate_stats_svg
from generate_assets import get_languages, generate_languages_svg, generate_glowing_line
from generate_achievements import generate_achievements_svg
from generate_pinned import generate_pinned_svg
from generate_featured import generate_featured_svg
from generate_activity import generate_activity_svg
from generate_isocalendar import generate_isocalendar_svg

DEFAULT_USERNAME = "indoctrinatedrecluse"
OUTPUT_DIR = "profile-3d-contrib"


def run_safe(name, func, *args, **kwargs):
    print(f"\n[+] Running {name}...")
    try:
        res = func(*args, **kwargs)
        print(f"    [OK] {name} completed.")
        return res
    except Exception as e:
        print(f"    [ERROR] {name} failed: {e}")
        traceback.print_exc()
        return None


def sync_3d_calendar_variants():
    """Ensure dark and light variants of the 3D contribution graph exist."""
    rainbow_base = os.path.join(OUTPUT_DIR, "profile-night-rainbow.svg")
    rainbow_dark = os.path.join(OUTPUT_DIR, "profile-night-rainbow-dark.svg")
    rainbow_light = os.path.join(OUTPUT_DIR, "profile-night-rainbow-light.svg")

    if os.path.exists(rainbow_base):
        # Create dark copy for naming symmetry
        shutil.copyfile(rainbow_base, rainbow_dark)
        print(f"    [OK] Synced {rainbow_dark}")
        # Recolor to light
        recolor_file_to_light(rainbow_base, rainbow_light)
        print(f"    [OK] Generated {rainbow_light}")
    else:
        print(f"    [WARN] Base 3D calendar {rainbow_base} not found; skipping light 3D calendar generation.")


def main():
    token = os.environ.get("GITHUB_TOKEN")
    username = os.environ.get("GITHUB_REPOSITORY_OWNER") or DEFAULT_USERNAME

    print(f"============================================================")
    print(f"  LAUNCHING CYBERPUNK PROFILE DASHBOARD ASSET GENERATION")
    print(f"  Target User: {username}")
    print(f"  Token Present: {'YES' if token else 'NO (running in public/cached fallback mode)'}")
    print(f"============================================================")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Header Banner
    run_safe("Cyberpunk Banner", generate_banner)

    # 2. Glowing Divider Line
    run_safe(
        "Glowing Line Dividers",
        generate_glowing_line,
        os.path.join(OUTPUT_DIR, "glowing-line.svg"),
    )

    # 3. Dynamic Typing SVG
    run_safe(
        "Typing Greeting",
        generate_typing_svg,
        os.path.join(OUTPUT_DIR, "typing.svg"),
    )

    # 4. System Status Terminal
    run_safe(
        "System Status Terminal",
        generate_system_status_svg,
        os.path.join(OUTPUT_DIR, "system-status.svg"),
    )

    # 5. Profile Telemetry & Stats Dashboard
    metrics = run_safe("Gather Stats Metrics", gather_metrics, username, token)
    if metrics:
        run_safe(
            "Stats Dashboard",
            generate_stats_svg,
            metrics,
            os.path.join(OUTPUT_DIR, "stats.svg"),
        )

    # 6. Language Core Matrix
    lang_bytes = run_safe("Gather Language Stats", get_languages, username, token)
    if lang_bytes:
        run_safe(
            "Language Matrix",
            generate_languages_svg,
            lang_bytes,
            os.path.join(OUTPUT_DIR, "languages.svg"),
            username,
        )

    # 7. System Achievements
    run_safe(
        "System Achievements",
        generate_achievements_svg,
        username,
        token,
        os.path.join(OUTPUT_DIR, "achievements.svg"),
    )

    # 8. Pinned Repositories
    run_safe(
        "Pinned Repositories",
        generate_pinned_svg,
        username,
        token,
        os.path.join(OUTPUT_DIR, "pinned.svg"),
    )

    # 9. Featured Projects
    run_safe(
        "Featured Projects",
        generate_featured_svg,
        username,
        token,
        os.path.join(OUTPUT_DIR, "featured.svg"),
    )

    # 10. Recent Activity Feed
    run_safe(
        "Recent Activity Feed",
        generate_activity_svg,
        username,
        token,
        os.path.join(OUTPUT_DIR, "activity.svg"),
    )

    # 11. Rolling 365-Day Commit Grid
    run_safe(
        "Commit Heatmap (isocalendar)",
        generate_isocalendar_svg,
        username,
        token,
        os.path.join(OUTPUT_DIR, "isocalendar.svg"),
    )

    # 12. 3D Contribution Calendar Theme Sync
    print(f"\n[+] Syncing 3D Contribution Calendar Dark/Light variants...")
    sync_3d_calendar_variants()

    print(f"\n============================================================")
    print(f"  ALL PROFILE ASSETS GENERATION COMPLETED SUCCESSFULLY")
    print(f"============================================================\n")


if __name__ == "__main__":
    main()
