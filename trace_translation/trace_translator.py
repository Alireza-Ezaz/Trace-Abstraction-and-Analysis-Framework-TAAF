import pandas as pd
import json
import glob
from trace_translation.event_translator import EventTranslator


class TraceTranslator:
    def __init__(self, filepath, is_first_file):
        """
        Initialize the TraceProcessor class with the CSV file path and a flag indicating if it is the first file.
        """
        self.df = pd.read_csv(filepath, dtype=str)
        self.filter_events()
        self.is_first_file = is_first_file

    def filter_events(self):
        """
        Filter events to include only those related to system calls, scheduling, and power management.
        @todo: Add more event types as needed.
        """
        self.df['Event type'] = self.df['Event type'].fillna('')
        self.df = self.df[self.df['Event type'].str.startswith(('syscall', 'sche', 'power'))]
    def translate_event(self, event_translator, row, event_type):
        """
        Use the event_translator to generate translations based on the type of event.
        """
        if hasattr(event_translator, f'translate_{event_type}'):
            return getattr(event_translator, f'translate_{event_type}')(row)
        return ""
    def run(self):
        """
        Process each event in the dataframe to generate a translation .
        """
        event_translator = EventTranslator(self.df)
        output_filename = '../trace_translation_output/event_translations.txt'
        mode = 'w' if self.is_first_file else 'a'
        trace_translations = []

        with open(output_filename, mode) as file:
            for index, row in self.df.iterrows():
                event_type = row['Event type']
                translation = self.translate_event(event_translator, row, event_type)
                if translation:
                    file.write(translation + "\n")
                    trace_string = ','.join([str(x) for x in row.values])
                    trace_translations.append({"trace": trace_string, "translation": translation})

        return trace_translations


if __name__ == "__main__":
    trace_descriptions_all = []
    files = ['../trace_data/run0_0.csv']  # Adjust path as needed + you can add more files

    for i, file_path in enumerate(files):
        print(f"Processing file: {file_path}")
        trace_translator = TraceTranslator(file_path, i == 0)
        trace_translations = trace_translator.run()
        trace_descriptions_all.extend(trace_translations)

    json_output_filename = '../trace_translation_output/event_translations.json'
    with open(json_output_filename, 'w') as json_file:
        json.dump({"traces": trace_descriptions_all}, json_file, indent=4)
