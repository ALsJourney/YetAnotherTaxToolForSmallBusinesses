'use client'

import React, { useState } from 'react'
import { createYear } from '../lib/api'

export default function AddYearForm() {
    const [year, setYear] = useState('')

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        try {
            await createYear({ year: parseInt(year) })
            setYear('')
            // You might want to refresh the year list here
        } catch (error) {
            console.error('Error creating year:', error)
        }
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div>
                <label htmlFor="year" className="block text-sm font-medium text-gray-700">
                    Year
                </label>
                <input
                    type="number"
                    id="year"
                    value={year}
                    onChange={(e) => setYear(e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                    required
                    min="2010"
                    max="2024"
                />
            </div>
            <button
                type="submit"
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
            >
                Add Year
            </button>
        </form>
    )
}

