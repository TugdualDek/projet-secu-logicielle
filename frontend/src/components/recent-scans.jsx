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

async function getRecentScans() {
  await new Promise((resolve) => setTimeout(resolve, 1000));
  return [
    {
      id: 1,
      url: "https://example.com",
      status: "Terminé",
      date: "2023-11-27",
    },
    { id: 2, url: "https://test.com", status: "En cours", date: "2023-11-28" },
    {
      id: 3,
      url: "https://demo.com",
      status: "En attente",
      date: "2023-11-28",
    },
  ];
}

export default async function RecentScans() {
  const scans = await getRecentScans();

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
          {scans.map((scan) => (
            <TableRow key={scan.id}>
              <TableCell className="font-medium text-white text-sm md:text-base">
                {scan.url}
              </TableCell>
              <TableCell>
                <Badge
                  variant={
                    scan.status === "Terminé"
                      ? "success"
                      : scan.status === "En cours"
                      ? "warning"
                      : "secondary"
                  }
                  className="text-xs md:text-sm whitespace-nowrap"
                >
                  {scan.status}
                </Badge>
              </TableCell>
              <TableCell className="text-white text-sm md:text-base hidden md:table-cell">
                {scan.date}
              </TableCell>
              <TableCell>
                {scan.status === "Terminé" ? (
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
                ) : scan.status === "En cours" ? (
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
