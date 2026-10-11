import runpy

files = ["part_b_m1_m2_counts.py", "part_c_binary_search.py",
         "part_d_master_theorem.py", "part_e_search_cases.py",
         "part_f_asymptotic_proof.py", "part_g_scalability.py"]

for name in files:
    print("=" * 60)
    print("Running", name)
    print("=" * 60)
    runpy.run_path(name)
    print()
