#!/bin/bash

BASE_URL="http://localhost:8080"

echo "GET /note/60 (Middle C)"
curl -s "$BASE_URL/note/60"
echo -e "\n"

echo "PUT /note/61"
curl -s -X PUT "$BASE_URL/note/61" -d '{"velocity":100}' -H "Content-Type: application/json"
echo -e "\n"

echo "GET /notes"
curl -s "$BASE_URL/notes"
echo -e "\n"

echo "DELETE /note/61"
curl -s -X DELETE "$BASE_URL/note/61"
echo -e "\n"

echo "POST /notes/reset"
curl -s -X POST "$BASE_URL/notes/reset"
echo -e "\n"
