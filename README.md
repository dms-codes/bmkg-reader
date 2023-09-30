# BMKG Weather Data Processor

This Python script is a data processing tool that fetches and processes weather forecast data from the Indonesian Meteorology, Climatology, and Geophysics Agency (BMKG) website. It retrieves XML files containing weather forecasts for different regions and extracts relevant information such as location coordinates, weather parameters, and timestamps.

## Prerequisites

Before you begin, make sure you have the following:

- Python installed on your system.
- Required Python libraries, including `xml.etree.ElementTree`, `requests`, `pandas`, and `BeautifulSoup (bs4)`. You can install them using the following command:

   ```bash
   pip install xml.etree.ElementTree requests pandas beautifulsoup4
   ```

## Usage

1. Clone this repository or download the script.

2. Open the script and make the following adjustments as needed:

   - Set the `callsign`, `loc`, and `apikey` variables in the script.
   - Modify the URLs in the `get_xml_files()` function to fetch the desired XML files. You can use the provided BMKG website URL as a starting point.

3. Run the script using the following command:

   ```bash
   python bmkg_weather_processor.py
   ```

4. The script will fetch and process the XML files, extracting weather forecast data for different regions.

5. The processed data is stored in a Pandas DataFrame named `df`.

## Example

The script processes weather data and creates a Pandas DataFrame with columns such as `area_id`, `lat`, `long`, `description`, `param_id`, `param_description`, `timerange_datetime`, `value`, and `unit`. Here's a simplified example of what the DataFrame might look like:

```plaintext
   area_id       lat        long   description param_id  ... timerange_datetime  value   unit
0  Aceh 6.166667  97.083333  Cuaca        1   ...  202309300200     Cerah  Cuaca
1  Aceh 6.166667  97.083333  Cuaca        2   ...  202309300800     Cerah  Cuaca
2  Aceh 6.166667  97.083333  Cuaca        1   ...  202309301400     Cerah  Cuaca
3  Aceh 6.166667  97.083333  Cuaca        2   ...  202309301900     Cerah  Cuaca
4  Aceh 6.166667  97.083333  Cuaca        1   ...  202309302000     Cerah  Cuaca
```

## Note

- The script fetches weather data from the BMKG website, so ensure that you have internet access to make HTTP requests.

- The script may require further customization depending on your specific data processing needs or the structure of the BMKG XML files.

- Data is saved to a Pickle file named "data.pickle" for further analysis or usage.

Feel free to explore and customize the script to suit your specific requirements or integrate it into other projects as necessary.
