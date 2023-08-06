import sys


def desc_options(parser):
    parser.add_argument(
        "--ffmpeg-location", default=None, help="Point to your custom ffmpeg file."
    )
    parser.add_argument(
        "--help",
        "-h",
        action="store_true",
        help="Print info about the program or an option and exit.",
    )
    parser.add_required("input", nargs="*", help="The path to file(s)")
    return parser


def main(sys_args=sys.argv[1:]):
    import auto_editor
    import auto_editor.vanparse as vanparse

    from auto_editor.utils.log import Log
    from auto_editor.ffwrapper import FFmpeg, FileInfo

    parser = vanparse.ArgumentParser(
        "desc",
        auto_editor.version,
        description="Print the video's metadata description.",
    )
    parser = desc_options(parser)

    log = Log()

    try:
        args = parser.parse_args(sys_args)
    except vanparse.ParserError as e:
        log.error(str(e))

    ffmpeg = FFmpeg(args.ffmpeg_location, debug=False)

    print("")
    for input_file in args.input:
        inp = FileInfo(input_file, ffmpeg)
        if "description" in inp.metadata:
            print(inp.metadata["description"], end="\n\n")
        else:
            print("No description.", end="\n\n")


if __name__ == "__main__":
    main()
