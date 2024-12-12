"use client";

import React, { useState } from "react";

export default function Tooltip({ children, content, className }) {
	const [isVisible, setIsVisible] = useState(false);

	return (
		<div
			className="relative inline-flex items-center group"
			onMouseEnter={() => setIsVisible(true)}
			onMouseLeave={() => setIsVisible(false)}
		>
			{children}

			{isVisible && (
				<div
					className={`absolute bottom-full mb-2 flex items-center justify-center whitespace-nowrap px-2 py-1 text-xs text-white bg-white/5 border border-white/10 backdrop-blur-md rounded-md shadow-lg ${className}`}
				>
					{content}
					<div className="absolute w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-white/10 bottom-[-5px] left-1/2 transform -translate-x-1/2 rotate-180"></div>
				</div>
			)}
		</div>
	);
}