import { Suspense } from "react";
import NewScanForm from "../components/new-scan-form";
import RecentScans from "../components/recent-scans";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function HomePage() {
  return (
    <div className="space-y-8">
      <h1 className="text-3xl md:text-5xl font-bold text-center mb-8 md:mb-12 text-white">
        Scanner de Vulnérabilités Web
      </h1>
      <Card className="bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg border-none shadow-xl">
        <CardHeader>
          <CardTitle className="text-2xl md:text-3xl font-semibold text-white">
            Nouveau Scan
          </CardTitle>
        </CardHeader>
        <CardContent>
          <NewScanForm />
        </CardContent>
      </Card>
      <Card className="bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg border-none shadow-xl">
        <CardHeader>
          <CardTitle className="text-2xl md:text-3xl font-semibold text-white">
            Historique des Scans
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Suspense
            fallback={
              <div className="text-center text-white">
                Chargement de l&apos;historique des scans...
              </div>
            }
          >
            <RecentScans />
          </Suspense>
        </CardContent>
      </Card>
    </div>
  );
}
