from ong_ppt_translator.traductor_sonnet_v3 import translate_powerpoint as main
import argparse


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--input_file", type=str, required=True)
    args.add_argument("--output_file", type=str, required=True)
    args.add_argument("--start", type=int, required=False)
    args.add_argument("--end", type=int, required=False)
    parsed_args = args.parse_args()
    main(parsed_args.input_file, parsed_args.output_file, start=parsed_args.start, end=parsed_args.end)
