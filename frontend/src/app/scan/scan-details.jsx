import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

// Cette fonction simule la récupération des détails d'un scan
async function getScanDetails(id) {
  await new Promise((resolve) => setTimeout(resolve, 1000)); // Simule un délai réseau
  return {
    id,
    url: "https://test.com",
    status: "Terminé",
    progress: 100,
    startDate: "2023-11-28 10:00:00",
    endDate: "2023-11-28 10:05:30",
    vulnerabilities: [
      {
        id: 1,
        name: "XSS",
        severity: "Élevée",
        description: "Vulnérabilité Cross-Site Scripting détectée",
      },
      {
        id: 2,
        name: "SQL Injection",
        severity: "Critique",
        description: "Vulnérabilité d'injection SQL détectée",
      },
    ],
  };
}

export default async function ScanDetails({ id }) {
  const scanDetails = await getScanDetails(id);

  return (
    <Card>
      <CardHeader>
        <CardTitle>{scanDetails.url}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex justify-between items-center">
          <span>Statut:</span>
          <Badge
            variant={scanDetails.status === "Terminé" ? "success" : "warning"}
          >
            {scanDetails.status}
          </Badge>
        </div>
        <div>
          <span>Date de début: {scanDetails.startDate}</span>
        </div>
        <div>
          <span>Date de fin: {scanDetails.endDate}</span>
        </div>
        {scanDetails.status === "En cours" && (
          <div>
            <Progress value={scanDetails.progress} className="w-full" />
            <p className="text-sm text-muted-foreground mt-1">
              {scanDetails.progress}% complété
            </p>
          </div>
        )}
        {scanDetails.status === "Terminé" && (
          <div>
            <h3 className="font-semibold text-lg mb-2">
              Vulnérabilités détectées:
            </h3>
            <ul className="space-y-4">
              {scanDetails.vulnerabilities.map((vuln) => (
                <li key={vuln.id} className="border p-4 rounded-md">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-medium">{vuln.name}</span>
                    <Badge
                      variant={
                        vuln.severity === "Critique" ? "destructive" : "warning"
                      }
                    >
                      {vuln.severity}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    {vuln.description}
                  </p>
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
