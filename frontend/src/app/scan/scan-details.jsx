import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { useEffect, useState } from 'react';
import { scanService } from '@/services/api';

export default function ScanDetails({ id }) { 
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const data = await scanService.getReport(id);
        setReport(data);
      } catch (error) {
        console.error('Erreur lors de la récupération du rapport:', error);
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchReport();
  }, [id]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>{report.url}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex justify-between items-center">
          <span>Statut:</span>
          <Badge
            variant={report.status === "Terminé" ? "success" : "warning"}
          >
            {report.status}
          </Badge>
        </div>
        <div>
          <span>Date de début: {report.startDate}</span>
        </div>
        <div>
          <span>Date de fin: {report.endDate}</span>
        </div>
        {report.status === "En cours" && (
          <div>
            <Progress value={report.progress} className="w-full" />
            <p className="text-sm text-muted-foreground mt-1">
              {report.progress}% complété
            </p>
          </div>
        )}
        {report.status === "Terminé" && (
          <div>
            <h3 className="font-semibold text-lg mb-2">
              Vulnérabilités détectées:
            </h3>
            <ul className="space-y-4">
              {report.vulnerabilities.map((vuln) => (
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
