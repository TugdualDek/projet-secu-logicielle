"use client";
import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import ScanDetails from "./scan-details";

function ScanContent() {
  const searchParams = useSearchParams();
  const scanId = searchParams.get("id");

  return <ScanDetails id={scanId} />;
}

export default function ScanPage() {
  return (
    <div className="space-y-8">
      <h1 className="text-3xl md:text-4xl font-bold text-center mb-8 text-white">
        Détails du Scan
      </h1>
      <Suspense
        fallback={
          <div className="text-center text-white">
            Chargement des détails du scan...
          </div>
        }
      >
        <ScanContent />
      </Suspense>
    </div>
  );
}
