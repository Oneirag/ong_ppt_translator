from ong_ppt_translator.traductor_sonnet_v3 import translate_powerpoint
import argparse

def main(input_file, output_file):
    translate_powerpoint(input_file, output_file)

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--input_file", type=str, required=True)
    args.add_argument("--output_file", type=str, required=True)
    parsed_args = args.parse_args()
    main(parsed_args.input_file, parsed_args.output_file)
