"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { scanService } from "@/services/api";

function ScanDetails() {
  const searchParams = useSearchParams();
  const scanId = searchParams.get("id");

  const [scan, setScan] = useState(null);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!scanId) return;

      try {
        const fetchedScan = await scanService.getScan(scanId);
        const fetchedReport = await scanService.getReport(scanId);
        setScan(fetchedScan);
        setReport(fetchedReport);
      } catch (err) {
        console.error("Erreur lors de la récupération des données :", err);
        setError("Impossible de charger les données pour ce scan.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [scanId]);

  if (!scanId) {
    return (
      <div className="text-center text-white">
        Aucun identifiant de scan fourni dans l&apos;URL.
      </div>
    );
  }

  if (loading) {
    return (
      <div className="text-center text-white">
        Chargement des détails du scan...
      </div>
    );
  }

  if (error) {
    return <div className="text-center text-red-500">Erreur : {error}</div>;
  }

  if (!scan || !report) {
    return (
      <div className="text-center text-white">
        Aucun détail disponible pour ce scan.
      </div>
    );
  }

  return (
    <Card className="bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg border-none shadow-xl">
      <CardHeader>
        <CardTitle>{scan.target}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <span>Statut: {scan.status}</span>
        </div>
        <div>
          <span>Date de début: {scan.created_at}</span>
        </div>
        <div>
          <span>Date de fin: {scan.completed_at}</span>
        </div>
        {report.map((vulnerability, index) => (
          <div key={index} className="vulnerability-card">
            <h3>{vulnerability.vulnerability_name}</h3>
            <p>
              <strong>Type :</strong> {vulnerability.vulnerability_type}
            </p>
            <p>
              <strong>Date :</strong> {vulnerability.created_at}
            </p>
            <div>
              <h4>Détails :</h4>
              <pre className="p-4 rounded">
                {JSON.stringify(JSON.parse(vulnerability.description), null, 2)}
              </pre>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

export default function ScanPage() {
  return (
    <div className="space-y-8">
      <h1 className="text-3xl md:text-4xl font-bold text-center mb-8 text-white">
        Détails du Scan
      </h1>
      <Suspense
        fallback={<div className="text-center text-white">Chargement...</div>}
      >
        <ScanDetails />
      </Suspense>
    </div>
  );
}
