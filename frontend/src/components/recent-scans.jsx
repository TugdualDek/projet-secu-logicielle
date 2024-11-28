"use client";
import Link from "next/link";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";
import { useEffect, useState, useCallback } from "react";
import { scanService } from "@/services/api";

export default function RecentScans() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [hasInProgress, setHasInProgress] = useState(false);

  // Fonction de récupération des scans
  const fetchScans = async () => {
    try {
      const data = await scanService.getAllScans();
      setScans(data);
      // Vérifie s'il y a des scans en cours
      setHasInProgress(data.some((scan) => scan.status === "in_progress"));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchScans();

    const handleScanCreated = () => {
      fetchScans();
      setHasInProgress(true);
    };
    window.addEventListener('scanCreated', handleScanCreated);

    const intervalId = setInterval(() => {
      if (hasInProgress) {
        fetchScans();
      }
    }, 2000);

    return () => {
      clearInterval(intervalId);
      window.removeEventListener('scanCreated', handleScanCreated);
    };
  }, [hasInProgress]);

  if (loading) return <div>Chargement...</div>;
  if (error) return <div>Erreur: {error}</div>;

  return (
    <div className="overflow-x-auto">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="text-white text-sm md:text-lg">URL</TableHead>
            <TableHead className="text-white text-sm md:text-lg">
              Statut
            </TableHead>
            <TableHead className="text-white text-sm md:text-lg hidden md:table-cell">
              Date
            </TableHead>
            <TableHead className="text-white text-sm md:text-lg">
              Action
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {scans
            .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
            .map((scan) => (
              <TableRow key={scan.id}>
                <TableCell className="font-medium text-white text-sm md:text-base">
                  {scan.target}
                </TableCell>
                <TableCell>
                  <Badge
                    variant={
                      scan.status === "completed"
                        ? "success"
                        : scan.status === "in_progress"
                        ? "warning"
                        : scan.status === "failed"
                        ? "destructive"
                        : "secondary"
                    }
                    className="text-xs md:text-sm whitespace-nowrap"
                  >
                    {scan.status === "pending"
                      ? "En attente"
                      : scan.status === "in_progress"
                      ? "En cours"
                      : scan.status === "failed"
                      ? "Échoué"
                      : "Terminé"}
                  </Badge>
                </TableCell>
                <TableCell className="text-white text-sm md:text-base hidden md:table-cell">
                  {scan.created_at}
                </TableCell>
                <TableCell>
                  {scan.status === "completed" ? (
                    <Button
                      asChild
                      variant="secondary"
                      size="sm"
                      className="text-xs md:text-sm"
                    >
                      <Link
                        href={{
                          pathname: "/scan",
                          query: {
                            id: scan.id,
                          },
                        }}
                      >
                        Voir Détails
                      </Link>
                    </Button>
                  ) : scan.status === "in_progress" ? (
                    <Loader2 className="h-4 w-4 md:h-5 md:w-5 animate-spin text-white" />
                  ) : null}
                </TableCell>
              </TableRow>
            ))}
        </TableBody>
      </Table>
    </div>
  );
}
