import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatbotComponent } from '../chatbot/chatbot.component';
import { NavbarComponent } from '../navbar/navbar.component';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';  // Import sanitizer for iframe

@Component({
  selector: 'app-knowledge',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ChatbotComponent,
    NavbarComponent,
  ],
  templateUrl: './knowledge.component.html',
  styleUrls: ['./knowledge.component.scss']
})
export class KnowledgeComponent implements OnInit {
  knowledgeResources: any;  // To store API data (articles, PDFs, videos)
  isLoading: boolean = false;
  customerId: string | null = '';
  sanitizedVideos: { title: string, url: SafeResourceUrl }[] = [];  // To store sanitized video URLs

  constructor(private http: HttpClient, private sanitizer: DomSanitizer) {}  // Inject DomSanitizer

  ngOnInit(): void {
    this.customerId = localStorage.getItem('customerId');
    this.fetchKnowledgeResources();
  }

  fetchKnowledgeResources(): void {
    this.isLoading = true;
    this.http.get(`http://localhost:5000/knowledge_center/${this.customerId}`).subscribe(
      (response: any) => {
        console.log('Knowledge Resources:', response);
        this.knowledgeResources = response;

        // Sanitize the video URLs
        if (response.Videos) {
          // Assuming each video in the response array is of the form [title, url]
          this.sanitizedVideos = response.Videos.map((video: [string, string]) => ({
            title: video[0],
            url: this.sanitizeUrl(this.convertToEmbedUrl(video[1])),
          }));
        }
        this.knowledgeResources = response;

        this.isLoading = false;
      },
      (error) => {
        console.error('Failed to fetch knowledge resources:', error);
        this.isLoading = false;
        alert('Error loading knowledge resources. Please try again later.');
      }
    );
  }
  convertToEmbedUrl(videoUrl: string): string {
    if (videoUrl.includes('youtube.com/watch?v=')) {
      return videoUrl.replace('watch?v=', 'embed/');
    } else if (videoUrl.includes('youtu.be/')) {
      // Handle shortened YouTube links like https://youtu.be/video_id
      return videoUrl.replace('youtu.be/', 'www.youtube.com/embed/');
    } else if (videoUrl.includes('instagram.com')) {
      // Handle Instagram embed links by converting them to iframe format
      return `${videoUrl}embed`;
    }else if (videoUrl.includes('cnbc.com/video/')) {
      // CNBC video embed link adjustment (if applicable)
      return videoUrl; // CNBC usually supports direct embedding
    }
    return videoUrl; // Return as-is if no known format detected
  }
  
  sanitizeUrl(url: string): SafeResourceUrl {
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);  // Sanitize URL for iframe
  }
}
