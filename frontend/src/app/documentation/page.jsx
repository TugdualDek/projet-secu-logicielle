import React from "react";
import { Card } from "@/components/ui/card";

export default function DocumentationPage() {
  return (
    <Card className="bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg border-none shadow-xl">
      <main className="container mx-auto p-4">
        <h1 className="text-3xl font-bold mb-6">Documentation du Scanner</h1>
        <div className="space-y-6">
          <section>
            <h2 className="text-2xl font-semibold mb-3">Introduction</h2>
            <p>
              Bienvenue dans la documentation du Scanner de Vulnérabilités Web.
              Cet outil est conçu pour aider les développeurs et les
              professionnels de la sécurité à identifier les vulnérabilités
              potentielles dans les applications web.
            </p>
          </section>
          <section>
            <h2 className="text-2xl font-semibold mb-3">
              Comment utiliser le scanner
            </h2>
            <ol className="list-decimal list-inside space-y-2">
              <li>Accédez à la page d&apos;accueil du scanner.</li>
              <li>
                Entrez l&apos;URL du site web que vous souhaitez analyser dans
                le champ prévu à cet effet.
              </li>
              <li>
                Cliquez sur le bouton &quot;Lancer le Scan&quot; pour démarrer
                l&apos;analyse.
              </li>
              <li>
                Attendez que le scan soit terminé. Vous pouvez suivre sa
                progression dans la section &quot;Historique des Scans&quot;.
              </li>
              <li>
                Une fois le scan terminé, cliquez sur &quot;Voir Détails&quot;
                pour accéder aux résultats complets.
              </li>
            </ol>
          </section>
          <section>
            <h2 className="text-2xl font-semibold mb-3">
              Types de vulnérabilités détectées
            </h2>
            <ul className="list-disc list-inside space-y-2">
              <li>Injection SQL</li>
              <li>Cross-Site Scripting (XSS)</li>
              <li>Cross-Site Request Forgery (CSRF)</li>
              <li>Mauvaise configuration de sécurité</li>
              <li>Failles d&apos;authentification</li>
              <li>Exposition de données sensibles</li>
            </ul>
          </section>
          <section>
            <h2 className="text-2xl font-semibold mb-3">
              Interprétation des résultats
            </h2>
            <p>
              Les résultats du scan sont présentés sous forme de liste de
              vulnérabilités détectées. Chaque vulnérabilité est accompagnée
              d&apos;une description, d&apos;un niveau de sévérité et de
              recommandations pour la correction.
            </p>
          </section>
          <section>
            <h2 className="text-2xl font-semibold mb-3">Bonnes pratiques</h2>
            <ul className="list-disc list-inside space-y-2">
              <li>
                Effectuez des scans réguliers pour maintenir la sécurité de
                votre application.
              </li>
              <li>
                Assurez-vous d&apos;avoir l&apos;autorisation nécessaire avant
                de scanner un site web.
              </li>
              <li>
                Utilisez les résultats du scan comme point de départ pour
                améliorer la sécurité de votre application.
              </li>
              <li>
                Consultez un expert en sécurité pour une analyse approfondie des
                vulnérabilités critiques.
              </li>
            </ul>
          </section>
        </div>
      </main>
    </Card>
  );
}
