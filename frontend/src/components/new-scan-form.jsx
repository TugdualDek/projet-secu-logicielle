"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { scanService } from '@/services/api';

export default function NewScanForm() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await scanService.createScan(url);
      window.dispatchEvent(new Event('scanCreated'));
    } catch (error) {
      console.error('Erreur lors de la création du scan:', error);
    } finally {
      setLoading(false);
      setUrl("");
    }
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
        disabled={loading}
      >
        {loading ? 'Création...' : 'Lancer le scan'}
      </Button>
    </form>
  );
}
