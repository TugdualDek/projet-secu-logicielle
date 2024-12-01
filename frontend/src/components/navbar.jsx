"use client";

import { useState } from "react";
import Link from "next/link";
import { Home, List, FileText, Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => setIsOpen(!isOpen);

  return (
    <nav className="w-[90%] mt-6 bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg rounded-2xl shadow-lg">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center space-x-3 text-white">
            <Home className="h-8 w-8" />
            <span className="font-bold text-xl md:text-2xl">
              Scanner de Vulnérabilités
            </span>
          </Link>
          <div className="hidden md:flex space-x-6">
            <NavLinks />
          </div>
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden text-white"
            onClick={toggleMenu}
          >
            <Menu className="h-6 w-6" />
            <span className="sr-only">Toggle menu</span>
          </Button>
        </div>
        <div
          className={cn(
            "md:hidden overflow-hidden transition-all duration-300 ease-in-out",
            isOpen ? "max-h-48 mt-4" : "max-h-0"
          )}
        >
          <div className="flex flex-col space-y-4">
            <NavLinks />
          </div>
        </div>
      </div>
    </nav>
  );
}

function NavLinks() {
  return (
    <>
      <NavLink href="/" icon={<Home className="h-5 w-5" />} text="Accueil" />
      <NavLink
        href="/documentation"
        icon={<FileText className="h-5 w-5" />}
        text="Documentation"
      />
      <NavLink
        href="https://github.com/TugdualDek/projet-secu-logicielle"
        icon={<List className="h-5 w-5" />}
        text="Code source"
      />
    </>
  );
}

function NavLink({ href, icon, text }) {
  return (
    <Link
      href={href}
      className="flex items-center space-x-2 text-white hover:text-green-200 transition-colors duration-200"
    >
      {icon}
      <span className="text-lg">{text}</span>
    </Link>
  );
}
