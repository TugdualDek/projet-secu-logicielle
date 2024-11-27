"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function NewScanForm() {
  const [url, setUrl] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Lancement d'un scan pour:", url);
    setUrl("");
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="url" className="text-white text-base md:text-lg">
          URL à scanner
        </Label>
        <Input
          id="url"
          type="url"
          placeholder="https://example.com"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
          className="bg-white bg-opacity-30 border-white border-opacity-50 text-white placeholder-white placeholder-opacity-75 text-sm md:text-lg"
        />
      </div>
      <Button
        type="submit"
        className="w-full bg-green-500 hover:bg-green-600 text-white text-sm md:text-lg"
      >
        Lancer le Scan
      </Button>
    </form>
  );
}
