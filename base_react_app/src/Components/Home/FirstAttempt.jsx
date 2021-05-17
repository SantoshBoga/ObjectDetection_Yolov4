import React, { Component } from 'react';
import Axios from 'axios';
import './FirstAttempt.styles.css'
// import imgurl from '../../detections'
// const requestImageFile = require.context('../../detections', true, /.jpg$/);

class FirstAttempt extends Component {
    state = {
        
        file_path: ""

    }
    inputChangeHandler = (e) => {
        e.preventDefault();
        const { value, name } = e.target;
        this.setState({ [name]: value });
    }
    // handleSubmit = (e) => {
    //     e.preventDefault();
    //     const postData = {
    //         ...this.state
    //     }
    //     // console.log(postData)
    //     Axios.defaults.headers.common['Authorization'] = this.props.jwtToken;

    //     Axios.post(`${routeConstants.BACKEND_URL}/restaurant${routeConstants.POST_MENU_ITEM}`, postData).then((res) => {
    //         console.log(res);
    //         window.alert("Created Successfully");
    //     }).catch((err) => {
    //         console.log(err)
    //         window.alert("Unable to create");
    //     })
    // }



    onFileUpload = e => {
        e.preventDefault();
        console.log(this.state)
        //  this.setState({ projectId: this.props.match.params.projectId })
        let formData = new FormData();

        formData.append("file", this.state.selectedFile);


        Axios
            .post(
                "http://127.0.0.1:5000/detection",
                formData
            )
            .then(response => {
                // let str=JSON.stringify(response.data).replace('"',""); 
                // let temp=response.data;
                // let imgVar=<img src={requestImageFile(`./${temp}`)} height='400' /> 
                this.setState({ file_path:response.data }, () => console.log(this.state))
                // setTimeout(()=>console.log(response),10000)
                // this.setState({ file_path: file, Maximum_Probability: str[1], Classified: classif }, () => console.log(this.state))
                // window.alert(JSON.stringify(response.data))
            })
            // .catch((err) => {
            //     console.log("Error" + err);
            //     window.alert("Error")
            // })
    };





    onFileChange = event => {
        event.preventDefault();
        this.setState({ selectedFile: event.target.files[0] });
        if (this.state.selectedFile) {
            this.setState({ app: this.state.selectedFile.name });
        }
    };

    render() {
        // let imageVar
        // let images = require.context('../../detections/', true);
        // let url
        // if (this.state.file_path !== "") {
            // url = images('./' + this.state.file_path)
            // url=require(`../../detections/${this.state.file_path}`)
            // imageVar =
                //  <img height='400' width='400' src="https://www.greenbiz.com/sites/default/files/images/articles/featured/plasticwastesstock.jpg"></img>
                // <div >
                    // <h6>Results</h6>

                    {/* <img src={{ url }} /> */}
                    {/* <h6> Probability: {this.state.Maximum_Probability}</h6>
                    <h6>Classification: {this.state.Classified}</h6> */}
                // </div>
            // console.log("image var")
        // }
        // let profileURL = `${routeConstants.BACKEND_URL}${this.state.image_url}`
        return (<div className="container">
            {/* <h4>Create Menu Item</h4> */}
            <h3>Beach Litter Classification and Detection</h3>
            <form className="formData" onSubmit={this.onFileUpload}>
                <div className="profile">
                    <div >

                        <div className="mb-3" >
                            <label for="formFile" className="form-label">File input</label>
                            <input className="form-control" type="file" id="formFile" onChange={this.onFileChange} />
                        </div>

                    </div>

                </div>

                <div >
                    <button type="submit" className="btn btn-danger">Upload</button>
                </div>

            </form>
            <div style={{ marginTop: "20px" }}>
                {/* Maximum Probability: {this.state.Maximum_Probability}
                Classification : {this.state.Classified} */}
                {/* {this.state.out} */}
                {/* {this.state.file_path} */}
                <img src={this.state.file_path} height='400' maxWidth="700" />

            </div>
        </div >);
    }
}

export default FirstAttempt;