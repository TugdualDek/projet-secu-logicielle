"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { ShieldAlert, ShieldCheck, ChevronDown } from 'lucide-react';

import SearchInput from '@/components/search-input';
import Badge from "@/components/badge";

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

// const accordionData = [
// 	{
// 		id: 1,
// 		badge: "1 Critical",
// 		title: "Access Control",
// 		subtitle: "Security subtitle quickly describing",
// 		description: "Lorem ipsum quick description of the issue here",
// 	},
// 	{
// 		id: 2,
// 		badge: "1 High",
// 		title: "Cryptography",
// 		subtitle: "Sensitive data",
// 		description: "Details about cryptography vulnerabilities and their impacts.",
// 	},
// 	{
// 		id: 3,
// 		badge: "1 Medium",
// 		title: "Injection",
// 		subtitle: "Security subtitle quickly describing",
// 		description: "No issues detected for Injection vulnerabilities.",
// 	},
// 	{
// 		id: 4,
// 		badge: "1 Low",
// 		title: "Name 4",
// 		subtitle: "Security subtitle quickly describing",
// 		description: "No issues detected for Injection vulnerabilities.",
// 	},
// 	{
// 		id: 5,
// 		badge: "No vulnerability",
// 		title: "Name 5",
// 		subtitle: "Security subtitle quickly describing",
// 		description: "No issues detected for Injection vulnerabilities.",
// 	},
// 	{
// 		id: 6,
// 		badge: "No vulnerability",
// 		title: "Name 6",
// 		subtitle: "Security subtitle quickly describing",
// 		description: "No issues detected for Injection vulnerabilities.",
// 	},
// 	{
// 		id: 7,
// 		badge: "No vulnerability",
// 		title: "Name 7",
// 		subtitle: "Security subtitle quickly describing",
// 		description: "No issues detected for Injection vulnerabilities.",
// 	}
// ];

const badgeVariantMapper = (badgeText) => {
	if (badgeText.toLowerCase().includes("critical")) return "critical";
	if (badgeText.toLowerCase().includes("high")) return "high";
	if (badgeText.toLowerCase().includes("medium")) return "medium";
	if (badgeText.toLowerCase().includes("low")) return "low";
	return "noVulnerability";
};

function ScanReport() {
	const searchParams = useSearchParams();
	const scanId = searchParams.get("id");

	const [scan, setScan] = useState(null);
	const [report, setReport] = useState(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);
	const [openAccordions, setOpenAccordions] = useState([]);

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
			<h1 className="text-white">
				Aucun identifiant de scan fourni dans l&apos;URL.
			</h1>
		);
	}
	
	if (loading) {
		return (
			<h1 className="text-white">
				Chargement des détails du scan...
			</h1>
		);
	}
	
	if (error) {
		return (
			<h1 className="text-red">
				Erreur : {error}
			</h1>
		);
	}
	
	if (!scan || !report) {
		return (
			<h1 className="text-white">
				Aucun détail disponible pour ce scan.
			</h1>
		);
	}

	// const vulnerabilitiesCount = accordionData.filter(
	// 	(item) => !item.badge.toLowerCase().includes("no vulnerability")
	// ).length;

	const vulnerabilitiesCount = report.length;

	const toggleAccordion = (id) => {
		// Toggle the accordion's ID in the array
		setOpenAccordions((prev) =>
			prev.includes(id) ? prev.filter((accordionId) => accordionId !== id) : [...prev, id]
		);
	};

	return (
		<div className='w-full max-w-[1200px] mx-auto min-h-screen flex flex-col items-center pt-[25vh] px-4 pb-4 gap-2'>
			
			{/* Alert Header */}
			<div className="h-16 w-16 flex items-center justify-center bg-red/15 backdrop-blur-md rounded-full border border-white/15">
				<ShieldAlert size={36} className='text-red' />
				<ShieldCheck size={36} className='text-green hidden'/>
			</div>

			<h1 className="text-5xl font-semibold py-4">
				{vulnerabilitiesCount === 0
					? "Good news! This page has no vulnerabilities!"
					: `Uh oh! This page has ${vulnerabilitiesCount} ${
						vulnerabilitiesCount === 1 ? "vulnerability" : "vulnerabilities"
					}!`}
			</h1>

			<SearchInput />

			<p className='mt-4 italic text-sm text-foreground-secondary'>
				Analyzed on <span className='font-semibold'>{scan.created_at}</span>
			</p>

			{/* Scan Status */}
			<div className="w-full text-center text-lg font-medium mt-4 text-white">
				<div>Statut: {scan.status === "completed" ? "Terminé" : "En cours"}</div>
				<div>Date de début: {scan.created_at}</div>
				<div>Date de fin: {scan.completed_at}</div>
			</div>

			{/* Accordion Grid */}
			<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 mt-16 w-full px-6">
				{report.map.map((vulnerability, index) => {
					let descriptionData = {};
					try {
						descriptionData = JSON.parse(vulnerability.description);
					} catch (error) {
						console.error("Erreur lors de l'analyse de la description :", error);
					}
					
					const isOpen = openAccordions.includes(index);
					const isVulnerable = findVulnerableField(descriptionData);
					// const badgeVariant = badgeVariantMapper(index);

					return (
						<div
							key={index}
							className={`flex flex-col justify-between group border border-white/15 rounded-lg p-8 gap-8 relative transition-all duration-300 hover:bg-white/5 cursor-pointer 
								${isOpen ? "col-span-1 sm:col-span-2 lg:col-span-3 bg-white/5" : "col-span-1"}
							`}
							onClick={() => toggleAccordion(index)}
						>
							<div className="flex w-full items-center justify-between">
								
								{/* Badge */}
								{/* <Badge variant={badgeVariant}>
									{item.badge}
								</Badge> */}
								
								{isVulnerable === true && (
									<Badge variant="critical">1 Critical</Badge>
								)}
								{isVulnerable === false && (
									<Badge variant="noVulnerability">No vulnerability</Badge>
								)}

								{/* Chevron */}
								<div className="opacity-0 transition duration-300 group-hover:opacity-100">
									<ChevronDown size={20} className="text-white" />
								</div>

							</div>

							{/* Title and Subtitle */}
							<div className="w-full flex flex-col items-start gap-2">
								<h2 className="text-white text-2xl font-semibold mt-2">
									{vulnerability.vulnerability_name}
								</h2>

								<p className="text-foreground-secondary text-sm">
									Type: {vulnerability.vulnerability_type}
								</p>

								{/* Paragraph */}
								{isOpen && (
									// <p className="text-white mt-4">
									// 	{item.description}
									// </p>
									<pre className="text-white mt-4 p-4 bg-black/20 rounded">
										{JSON.stringify(descriptionData, null, 2)}
									</pre>
								)}
							</div>
						</div>
					);
				})}
			</div>
		</div>
	);
};

export default function Scan() {
	return (
		<div className="w-full h-auto text-center text-4xl font-semibold flex flex-col items-center justify-center p-4">
			<Suspense
				fallback={<div className="text-center text-white">Chargement...</div>}
			>
				<ScanReport />
			</Suspense>
		</div>
	);
}