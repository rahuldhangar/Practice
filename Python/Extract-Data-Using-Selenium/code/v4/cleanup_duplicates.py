"""
Utility script to clean up duplicate records from existing Excel files
====================================================================
This script removes duplicate records based on Name + District combination
"""
import pandas as pd
import os

def remove_duplicates_from_excel(filename):
    """Remove duplicates from Excel file and save cleaned version"""
    if not os.path.exists(filename):
        print(f"❌ File {filename} not found!")
        return
    
    print(f"🔍 Analyzing {filename}...")
    
    # Load data
    df = pd.read_excel(filename)
    original_count = len(df)
    print(f"📊 Original records: {original_count}")
    
    # Remove duplicates based on Name and District
    df_cleaned = df.drop_duplicates(subset=['Name', 'District'], keep='first')
    cleaned_count = len(df_cleaned)
    duplicates_removed = original_count - cleaned_count
    
    if duplicates_removed > 0:
        print(f"🧹 Removed {duplicates_removed} duplicate records")
        print(f"✅ Clean records: {cleaned_count}")
        
        # Save cleaned version
        backup_filename = filename.replace('.xlsx', '_backup.xlsx')
        print(f"💾 Creating backup: {backup_filename}")
        df.to_excel(backup_filename, index=False)
        
        print(f"💾 Saving cleaned data to: {filename}")
        df_cleaned.to_excel(filename, index=False)
        
        print("🎉 Cleanup completed successfully!")
    else:
        print("✅ No duplicates found. File is already clean!")

if __name__ == "__main__":
    # Clean up the v3 output file if it exists
    cleanup_files = [
        "Judicial_Officers_MP_v3.xlsx",
        "jo_mp.xlsx", 
        "judicial_officers_madhya_pradesh.xlsx"
    ]
    
    print("=" * 60)
    print("🧹 Duplicate Cleanup Utility for Judicial Officers Data")
    print("=" * 60)
    
    for filename in cleanup_files:
        if os.path.exists(filename):
            remove_duplicates_from_excel(filename)
            print("-" * 60)
    
    print("🏁 Cleanup process completed!")
