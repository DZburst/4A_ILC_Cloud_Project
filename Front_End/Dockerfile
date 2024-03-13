# Use Nginx base image
FROM nginx:alpine

# Copy static files to Nginx server
COPY ./ /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
