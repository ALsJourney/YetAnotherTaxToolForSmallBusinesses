import YearList from './components/YearList'
import AddYearForm from './components/AddYearForm'

export default function Home() {
  return (
      <main className="container mx-auto p-4">
        <h1 className="text-3xl font-bold mb-4">Yet Another Tax Tool for Small Businesses</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h2 className="text-2xl font-semibold mb-2">Years</h2>
            <YearList />
          </div>
          <div>
            <h2 className="text-2xl font-semibold mb-2">Add New Year</h2>
            <AddYearForm />
          </div>
        </div>
      </main>
  )
}

