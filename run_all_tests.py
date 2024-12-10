import h1_tag_exists
import currency_filtering
import html_tag_sequence
import image_alt_attribute
import script_data
import url_status_test

if __name__ == "__main__":
    print("Running H1 Tag Test...")
    h1_tag_exists.main()
    
    print("Running Currency Filtering Test...")
    currency_filtering.main()
    
    print("Running HTML Tag Sequence Test...")
    html_tag_sequence.main()
    
    print("Running Image Alt Attribute Test...")
    image_alt_attribute.main()
    
    print("Running Script Data Test...")
    script_data.main()
    
    print("Running URL Status Test...")
    url_status_test.main()
    
    print("All tests completed. Results saved in 'reports/test_results.xlsx'.")
