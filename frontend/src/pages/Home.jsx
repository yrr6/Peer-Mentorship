// frontend/src/pages/Home.jsx
import { useEffect, useState } from "react";
import client from "../api/client"; // Axios client
import PostCard from "../components/PostCard";

export default function Home() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    client.get("/posts") // Adjust endpoint if needed
      .then(res => {
        setPosts(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setError("Failed to fetch posts.");
        setLoading(false);
      });
  }, []);

  if (loading) return <p className="text-center mt-10">Loading posts...</p>;
  if (error) return <p className="text-center mt-10 text-red-500">{error}</p>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Recent Posts</h1>
      {posts.length === 0 ? (
        <p>No posts available.</p>
      ) : (
        <div className="grid gap-4">
          {posts.map(post => (
            <PostCard key={post.id} post={post} />
          ))}
        </div>
      )}
    </div>
  );
}
