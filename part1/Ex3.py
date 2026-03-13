def build_student_profile(**kwargs):
    # Set default values for missing keys
    profile = {
        "name": kwargs.get("name", "Unknown"),
        "age": kwargs.get("age", 0),
        "major": kwargs.get("major", "Undeclared"),
        "grades": kwargs.get("grades", [])
    }
    
    # Add a derived key based on age
    if profile["age"] < 18:
        profile["status"] = "Minor"
    else:
        profile["status"] = "Adult"
        
    return profile

if __name__ == "__main__":
    print("--- Testing Student Profile Builder ---")
    
    # Test 1: Full information
    student1 = build_student_profile(name="Hamza", age=24, major="ISE", grades=[10, 16])
    print(f"Profile 1: {student1}")
    
    # Test 2: Missing information (will use defaults)
    student2 = build_student_profile(name="Sarah", age=16)
    print(f"Profile 2: {student2}")
    
    # Test 3: Totally empty
    student3 = build_student_profile()
    print(f"Profile 3: {student3}")