import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import * as bcrypt from 'bcryptjs';

@Injectable({
  providedIn: 'root'
})
export class ApiCallsService {

  baseURL = "http://localhost:8080"

  constructor(private http: HttpClient) { }

  login(username:string,password:string){

    const salt = bcrypt.genSaltSync(10);
    const hashedpass = bcrypt.hashSync(password, salt);
    const url = this.baseURL+"/api/auth/gsn/login"

    const body = {
      "username":username,
      "password":hashedpass
    }

    return this.http.post<any>(url,body)
  }

  getusers(){
    const url = this.baseURL+"/api/gsn/voter/pending"
    return this.http.get<any>(url)
  }

  updatevoter(payload:any,sign:string){
    const url = this.baseURL+"/api/gsn/voter/verify"
    return this.http.post<any>(url,{
      "payload":payload,
      "sign":sign
    })
  }
}




