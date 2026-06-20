export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-zinc-950 text-white font-sans">
      <main className="flex flex-col items-center gap-8 px-8 text-center">
        <h1 className="text-5xl font-bold tracking-tight">
          Kanjo
          <span className="ml-3 text-2xl font-normal text-zinc-400">勘定</span>
        </h1>
        <p className="max-w-md text-lg text-zinc-400">
          JPYC決済の経費精算を、AIが30秒で。
        </p>
        <p className="max-w-sm text-sm text-zinc-500">
          Stablecoin expense tracking powered by Gemini AI
        </p>
        <div className="mt-4 rounded-full border border-zinc-700 px-6 py-3 text-sm text-zinc-500">
          Coming soon
        </div>
      </main>
    </div>
  );
}
