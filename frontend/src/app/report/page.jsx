"use client";

import { useState } from "react";
import SearchInput from '@/components/search-input';
import { ShieldAlert, ShieldCheck, ChevronDown } from 'lucide-react';

const accordionData = [
	{
		id: 1,
		badge: "1 Critical",
		title: "Access Control",
		subtitle: "Security subtitle quickly describing",
		description: "Lorem ipsum quick description of the issue here",
	},
	{
		id: 2,
		badge: "1 High",
		title: "Cryptography",
		subtitle: "Sensitive data",
		description: "Details about cryptography vulnerabilities and their impacts.",
	},
	{
		id: 3,
		badge: "No vulnerability",
		title: "Injection",
		subtitle: "Security subtitle quickly describing",
		description: "No issues detected for Injection vulnerabilities.",
	},
	{
		id: 4,
		badge: "No vulnerability",
		title: "Injection",
		subtitle: "Security subtitle quickly describing",
		description: "No issues detected for Injection vulnerabilities.",
	},
	{
		id: 5,
		badge: "No vulnerability",
		title: "Injection",
		subtitle: "Security subtitle quickly describing",
		description: "No issues detected for Injection vulnerabilities.",
	}
];

const Report = () => {
	const [openAccordion, setOpenAccordion] = useState(null);

	const toggleAccordion = (id) => {
		setOpenAccordion(openAccordion === id ? null : id);
	};

	return (
		<div className='w-full max-w-[1200px] mx-auto h-auto min-h-screen flex flex-col items-center pt-[25vh] px-4 pb-4 gap-2'>
			{/* Alert Header */}
			<div className="h-16 w-16 flex items-center justify-center bg-red/15 backdrop-blur-md rounded-full border border-white/15">
				<ShieldAlert size={36} className='text-red' />
				<ShieldCheck size={36} className='text-green hidden'/>
			</div>

			<h1 className='text-5xl py-4'>
				Uh oh! This page has 2 vulnerabilities!
			</h1>

			<SearchInput />

			<p className='mt-4 italic text-sm text-[#83848E]'>
				Analyzed on <span className='font-semibold'>5 Dec, 2024</span>
			</p>

			{/* Accordion Grid */}
			<div className="grid grid-cols-2 gap-2 mt-16 w-full px-6">
				{accordionData.map((item) => (
				<div
					key={item.id}
					className={`flex flex-col justify-between group border border-white/15 rounded-lg p-8 gap-8 relative transition-all duration-300 hover:bg-white/5 cursor-pointer
						${openAccordion === item.id ? "col-span-2" : "col-span-1"} 
					}`}
					onClick={() => toggleAccordion(item.id)}
				>
					<div className="flex flex-row w-full items-center justify-between">
						{/* Badge */}
						<span className="text-xs font-semibold uppercase text-red-400">
							{item.badge}
						</span>

						{/* Chevron */}
						<div className="opacity-0 transition duration-300 group-hover:opacity-100">
							<ChevronDown size={20} className="text-white" />
						</div>
					</div>

					{/* Title and Subtitle */}
					<div className="w-full flex flex-col items-start gap-2">
						<h2 className="text-white text-2xl font-semibold mt-2">
							{item.title}
						</h2>
						<p className="text-foreground-secondary text-sm">
							{item.subtitle}
						</p>

						{/* Paragraph */}
						{openAccordion === item.id && (
						<p className="text-white mt-4">
							{item.description}
						</p>
						)}
					</div>

				</div>
				))}
			</div>
		</div>
	);
};

export default Report;