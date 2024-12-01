"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import { scanService } from "@/services/api";

function findVulnerableField(data) {
  if (typeof data !== "object" || data === null) {
    return undefined;
  }

  if (data.hasOwnProperty("vulnerable")) {
    return data.vulnerable;
  }

  for (let key in data) {
    if (data.hasOwnProperty(key)) {
      const value = data[key];
      const result = findVulnerableField(value);
      if (typeof result !== "undefined") {
        return result;
      }
    }
  }

  return undefined;
}

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
        <CardTitle className="text-white">Cible : {scan.target}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4 text-white">
        <div>
          <span>
            Statut: {scan.status === "completed" ? "Terminé" : "En cours"}
          </span>
        </div>
        <div>
          <span>Date de début: {scan.created_at}</span>
        </div>
        <div>
          <span>Date de fin: {scan.completed_at}</span>
        </div>
        {report.map((vulnerability, index) => {
          let descriptionData = {};
          try {
            descriptionData = JSON.parse(vulnerability.description);
          } catch (error) {
            console.error(
              "Erreur lors de l'analyse de la description :",
              error
            );
          }

          const isVulnerable = findVulnerableField(descriptionData);

          return (
            <div key={index} className="vulnerability-card">
              <h3>
                <strong>Vulnérabilité :</strong>{" "}
                {vulnerability.vulnerability_name}
              </h3>
              <p>
                <strong>Type :</strong> {vulnerability.vulnerability_type}
              </p>
              {isVulnerable === true && (
                <Badge variant="destructive">Vulnérabilité potentielle</Badge>
              )}
              {isVulnerable === false && (
                <Badge variant="secondary">Vulnérabilité non identifiée</Badge>
              )}
              <div>
                <Accordion type="single" collapsible>
                  <AccordionItem value={`item-${index}`}>
                    <AccordionTrigger>Voir les détails</AccordionTrigger>
                    <AccordionContent>
                      <pre className="p-4 rounded">
                        {JSON.stringify(descriptionData, null, 2)}
                      </pre>
                    </AccordionContent>
                  </AccordionItem>
                </Accordion>
              </div>
            </div>
          );
        })}
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
