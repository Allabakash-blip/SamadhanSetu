# SIH Frontend — Milestone 1

```powershell
cd frontend
npm install
```

Copy `.env.example` to `.env`:

```env
VITE_API_URL=http://localhost:8000/api
VITE_GOOGLE_CLIENT_ID=your_google_client_id
```

Run:

```powershell
npm run dev
```

Usually Vite opens on http://localhost:5173.

Google Client ID is public. Never put GOOGLE_CLIENT_SECRET in this file.
