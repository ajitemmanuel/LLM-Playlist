import asyncio
import os
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport


async def main():
    # Get the current script directory
    script_path = Path(__file__).resolve()
    demo_root = script_path.parent / "demo"  # ✅ updated to match your folder structure
    project_root = demo_root / "project"
    project_root_uri = project_root.as_uri()
    print(f"📂 Project Folder: {project_root}, {project_root_uri}")
    

    transport = StreamableHttpTransport(url="http://127.0.0.1:8000/mcp/")
    
    roots = [
        # f"file://{project_root}",  # ✅ use full file:// path
        project_root_uri
    ]

    client = Client(transport, roots=roots)

    async with client:
        result = await client.call_tool("find_file", {"filename": "helper.py"})
        print("✅ Found paths:")
        if not result:
            print("  (no matches)")
        # for r in result:
        #     print("  -", r.text)
        print(result)


if __name__ == "__main__":
    asyncio.run(main())