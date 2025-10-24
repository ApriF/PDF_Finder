



# CLI shim
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Batched DOI harvester: staged downloads → processing → routed outputs")
    ap.add_argument("--config", required=True, help="Path to YAML config")
    args = ap.parse_args()
    asyncio.run(run(args.config))
