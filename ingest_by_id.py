import argparse

from services.ingest_base import ingest

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="Ingest tournaments by EMA id")
    argparser.add_argument("start", type=int, help="Starting tournament EMA id")
    argparser.add_argument("end", type=int, help="Ending tournament EMA id")
    args = argparser.parse_args()
    for ema_id in range(args.start, args.end):
        ingest(ema_id)