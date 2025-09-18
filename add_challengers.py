# add_challengers.py
import pandas as pd

# --- 10 Challenger articles are now included directly in this script ---
raw_articles = """
A new report from the maritime analytics group 'Nautical Futures Initiative' suggests that a shift in Arctic salinity levels is causing minor but significant deviations in global shipping routes. The report, titled "The Salt Compass," claims that the changes, while not dangerous, could increase fuel consumption for cargo vessels by up to 2% on major transatlantic routes. "We're seeing a subtle but persistent hydrographic change," stated Dr. Aris Thorne, a co-author of the report. "It's an economic issue more than an environmental one at this stage." Major shipping lines have not yet commented on the findings.

Sources within the Belgian Ministry of Economic Affairs have indicated that the government is considering a novel "digital tax" on automated financial trading algorithms. The proposal, allegedly drafted last month, would levy a micro-tax of 0.001% on every high-frequency trade executed within the country. Proponents argue the tax could generate over €50 million annually for infrastructure projects. However, a memo from the 'Brussels Financial Guild' warns that such a move could drive algorithmic trading firms to other European hubs like Frankfurt or Dublin.

Researchers at the University of Stralsund in Germany have announced a potential breakthrough in biodegradable plastics using a compound derived from chitin, a polymer found in crustacean shells. The new material reportedly decomposes in soil within 90 days, leaving behind only nitrogen-rich fertilizer. Dr. Lena Hartwig, lead researcher, was quoted in a university press release, saying, "This could fundamentally change how we approach single-use packaging." However, the process currently requires more energy than traditional plastic manufacturing, presenting a significant hurdle for commercial viability.

The Canadian and Japanese governments are in quiet negotiations to resolve a minor trade dispute over the export of specialty lumber, according to an unnamed official in Ottawa. The issue revolves around new Japanese import standards for cedar wood, which Canadian suppliers claim are unnecessarily restrictive and favor domestic producers. "It's a technicality, but it's affecting a niche but valuable market," the source said. A formal statement is expected after a bilateral trade commission meeting next week.

A think-tank known as the 'Global Labor Institute' has published a study indicating a surprising decline in productivity among remote workers who use more than two monitors. The study, which surveyed 5,000 workers across the tech sector, suggests that "information fragmentation" across multiple screens leads to a 5-8% increase in task completion times. The findings contradict the widely held belief that more screen real estate boosts efficiency.

Argentinian archaeologists have reportedly discovered a series of pre-Columbian geoglyphs in the remote Calchaquí Valleys. The markings, visible only from high altitude, do not resemble known Incan or Andean patterns. Dr. Mateo Costa, who allegedly leads the expedition, told a local newspaper, "The patterns suggest a culture with a sophisticated understanding of astronomy that we have no prior record of." The National Institute of Anthropology and Latin American Thought has yet to officially confirm the discovery.

The Swiss Federal Office for Agriculture is reportedly considering stricter regulations on the import of non-native honeybee species for agricultural pollination. A leaked internal report expresses concern that Italian and Carniolan bees may be out-competing local Swiss black bee populations, potentially impacting the biodiversity of alpine flora. The 'Swiss Beekeepers Association' has been lobbying for such protections, claiming that native pollinators are more effective for local fruit crops like apples and pears.

A new study by the 'Digital Ergonomics Research Consortium' claims that the increasingly popular curved computer monitors may contribute to a specific type of eye strain not seen with flat screens. The report suggests the subtle distortion of straight lines at the screen's periphery requires constant micro-adjustments from the eye's ciliary muscles. "We're not saying they are harmful, but the long-term effects of this new focal demand are not yet fully understood," the report summary stated.

The government of Estonia is set to pilot a new "digital notary" system using blockchain technology to authenticate public records. The initiative aims to reduce bureaucratic delays in property transfers and business registration. "This moves state-level authentication into the 21st century, making it more secure and instantly verifiable," said a spokesperson for the Ministry of Economic Affairs and Communications. The initial pilot program will run for six months in the city of Tartu.

Oceanographers from the 'Lisbon Institute for Marine Sciences' have reported observing an unusual deep-sea coral bleaching event off the coast of the Azores archipelago. Unlike tropical bleaching linked to warmer surface waters, this event is occurring at depths of over 500 meters. Lead scientist Dr. Ines Tavares suggests the cause may be a temporary shift in the deep-ocean oxygen minimum zone, a phenomenon not previously observed in the Atlantic. "The ecosystem at that depth is highly sensitive, so this is a significant, if puzzling, development," she noted.
"""

# --- SCRIPT LOGIC (No need to edit below this line) ---

print("Starting to add challenger articles...")

# Split the raw text into individual articles, filtering out any empty lines
challenger_articles = [article.strip() for article in raw_articles.strip().split('\n\n') if article.strip()]

if len(challenger_articles) < 10:
    print("\n--- WARNING ---")
    print(f"Detected only {len(challenger_articles)} articles. Please ensure 10 articles are in the text block.")
else:
    try:
        # Create a new DataFrame for the challenger articles
        new_data = {
            'text': challenger_articles,
            'label': ['fake'] * len(challenger_articles),
            'source': ['challenger'] * len(challenger_articles)
        }
        df_new = pd.DataFrame(new_data)

        # Open the existing test_data.csv and append the new rows
        df_original = pd.read_csv('test_data.csv')
        df_combined = pd.concat([df_original, df_new], ignore_index=True)
        
        # Save the updated DataFrame back to the CSV
        df_combined.to_csv('test_data.csv', index=False)
        
        print(f"\nSuccessfully added {len(df_new)} challenger articles.")
        print(f"Your 'test_data.csv' file now has a total of {len(df_combined)} rows.")
        print("\n✅ Phase 1 is now complete! You are ready for Phase 2: Prompt Engineering.")

    except FileNotFoundError:
        print("\n--- ERROR ---")
        print("Could not find 'test_data.csv'. Make sure this script is in the same folder.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")