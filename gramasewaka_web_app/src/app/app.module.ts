import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import {MatButtonModule,MatIconButton} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatInputModule} from '@angular/material/input';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LoginContainerComponent } from './uis/containers/login-container/login-container.component';
import { HomeComponent } from './uis/containers/home/home.component';
import { UserDashboardComponent } from './uis/containers/user-dashboard/user-dashboard.component';
import { BoxButtonComponent } from './uis/elements/box-button/box-button.component'
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent,
    LoginContainerComponent,
    HomeComponent,
    UserDashboardComponent,
    BoxButtonComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatButtonModule,
    MatInputModule,
    BrowserAnimationsModule,
    MatIconModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
 