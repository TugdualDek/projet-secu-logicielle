"use client";

const badgeVariants = {
    critical: "text-[#D0021B] bg-[#D0021B]/15",
    high: "text-[#CA5704] bg-[#CA5704]/15",
    medium: "text-[#FDB447] bg-[#FDB447]/15",
    low: "text-[#DFD78E] bg-[#DFD78E]/15",
    noVulnerability: "text-[#FFFFFF] bg-[#FFFFFF]/15",
};

const Badge = ({ variant = "noVulnerability", children }) => {
    return (
        <span
        className={`text-xs font-medium capitalize py-1 px-2 rounded-lg ${badgeVariants[variant]}`}
        >
        {children}
        </span>
    );
};

export default Badge;