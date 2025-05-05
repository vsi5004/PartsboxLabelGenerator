# PartsBox Labelmaker

A web-based label generator for organizing electronic parts using your [PartsBox](https://partsbox.com) inventory. Paste a PartsBox part URL or part ID, and it will:

- Look up the part's storage location via the PartsBox API
- Generate a printable label with a QR code and location
- Allow batch printing of multiple labels in one go to remove "buffer" space added by label maker between prints

The goal of this project is to allow me to print off multiple labels for SMD parts storage containers on a 12mm label while still retaining smartphone QR Code redability and a human-readable storage location label. 

---

## Project Structure

```
.
├── backend/
│   ├── main.py             # FastAPI backend
│   ├── partsbox.py         # PartsBox API calls and caching
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # React app
│   │   ├── components/
│   │   │   └── Label.jsx   # Single label component
│   │   └── main.jsx        # Vite entrypoint
│   ├── index.html
│   ├── styles.css
│   └── vite.config.mjs     # Vite config (ESM)
├── .env                    # API key config
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Compose config
└── README.md
```

---

## Technologies Used

| Component     | Purpose                            |
|---------------|------------------------------------|
| FastAPI       | Python backend and API server      |
| React         | Frontend UI                        |
| Vite          | Frontend build tool                |
| Docker        | Containerized deployment           |
| PartsBox API  | Retrieve part storage information  |

---

## PartsBox API Integration

This application uses the [PartsBox HTTP API](https://partsbox.com/api.html) to:

1. Retrieve part metadata via `POST /part/get`
2. Resolve storage location names via `POST /storage/get`

You will need a PartsBox API key, which can be generated in the PartsBox interface under **Settings → Data Access**.

---

### Adding Your API Key

Create a file called `.env` in the root of the project and add:

```env
PARTSBOX_API_KEY=your_partsbox_api_key_here
```

This value is passed into the Docker container automatically via `docker-compose.yml`.

---

## Build and Run with Docker

### Step 1: Clone the project

```bash
git clone https://github.com/vsi5004/partsbox-labelmaker.git
cd partsbox-labelmaker
```

### Step 2: Add your `.env` file

```bash
echo 'PARTSBOX_API_KEY=your_key_here' > .env
```

### Step 3: Build and start the application

```bash
docker compose up --build --force-recreate
```

Visit [http://localhost:8000](http://localhost:8000) in your browser.

---

## How to Use

1. Paste a PartsBox part URL or part ID (e.g. `cs444dyw0mk108k2d4csmkmpsk`)
2. Click "Fetch Location"
3. Optionally edit the location name
4. Click "Add to Queue" to queue the label
5. Add as many labels as needed
6. Click "Print" to print only the labels area

Each label includes:

- A QR code with the stripped URL to minimize the size of the QR code (no https:// prefix)
- A user-editable storage location name

---

## Cleanup

To stop the containers and remove unused Docker images:

```bash
docker compose down
docker image prune -f
```

---

## License

MIT License

Copyright (c) Ivan Iakimenko

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the “Software”), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in  
all copies or substantial portions of the Software.
, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING  
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER  
DEALINGS IN THE SOFTWARE.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED