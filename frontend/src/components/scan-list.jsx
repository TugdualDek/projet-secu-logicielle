import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

// Cette fonction simule la récupération des données de scan
// Dans une vraie application, vous feriez un appel API ici
async function getScanData() {
  await new Promise((resolve) => setTimeout(resolve, 1000)); // Simule un délai réseau
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

export default async function ScanList() {
  const scans = await getScanData();

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>URL</TableHead>
          <TableHead>Statut</TableHead>
          <TableHead>Date</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {scans.map((scan) => (
          <TableRow key={scan.id}>
            <TableCell>{scan.url}</TableCell>
            <TableCell>
              <Badge
                variant={
                  scan.status === "Terminé"
                    ? "success"
                    : scan.status === "En cours"
                    ? "warning"
                    : "secondary"
                }
              >
                {scan.status}
              </Badge>
            </TableCell>
            <TableCell>{scan.date}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
