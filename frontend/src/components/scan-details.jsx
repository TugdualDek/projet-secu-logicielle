import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

// Cette fonction simule la récupération des détails d'un scan
// Dans une vraie application, vous feriez un appel API ici
async function getScanDetails() {
  await new Promise((resolve) => setTimeout(resolve, 1000)); // Simule un délai réseau
  return {
    id: 2,
    url: "https://test.com",
    status: "En cours",
    progress: 65,
    vulnerabilities: [
      { id: 1, name: "XSS", severity: "Élevée" },
      { id: 2, name: "SQL Injection", severity: "Critique" },
    ],
  };
}

export default async function ScanDetails() {
  const scanDetails = await getScanDetails();

  return (
    <Card>
      <CardHeader>
        <CardTitle>{scanDetails.url}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="mb-2">Statut: {scanDetails.status}</p>
        {scanDetails.status === "En cours" && (
          <div className="mb-4">
            <Progress value={scanDetails.progress} className="w-full" />
            <p className="text-sm text-muted-foreground mt-1">
              {scanDetails.progress}% complété
            </p>
          </div>
        )}
        {scanDetails.status === "Terminé" && (
          <div>
            <h3 className="font-semibold mb-2">Vulnérabilités détectées:</h3>
            <ul className="list-disc pl-5">
              {scanDetails.vulnerabilities.map((vuln) => (
                <li key={vuln.id}>
                  {vuln.name} - Sévérité: {vuln.severity}
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
