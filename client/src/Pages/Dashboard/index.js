import React, { Component, Fragment } from 'react'
import { connect } from 'react-redux'
import Favicon from 'react-favicon';
import { Layout, Input, Icon, Upload, Card, Col, Row, Select } from 'antd'
import { getStore, getItem, getItemDetail, getCategory } from '../../Actions/ActionTypes';
import List from './component/List'
import groceries from './assets/groceries.svg'
import food from './assets/food.svg'
import favicon from './assets/favicon.ico'

const { Content, Sider } = Layout;
const { Dragger } = Upload;
const { Meta } = Card;
const { Option } = Select;

class Dashboard extends Component {

    constructor(props) {
        super(props);
        this.state = {
            greeting: true,
            dashboard: false,
            collapsed: false,
            view: 'store',
            searchBy: 'store'
        }
    }

    componentDidMount() {
        const { dispatch } = this.props
        dispatch(getStore({ search: "" }))
        dispatch(getCategory({}))
    }

    render() {
        const { greeting, dashboard, collapsed, view, searchBy } = this.state
        const { store, item, itemDetail, category, dispatch } = this.props
        return (
            <Layout className="dashboard-wrapper">
                <Favicon url={favicon} />
                {greeting && <Content className="dashboard-intro" onClick={() => this.setState({ greeting: false, dashboard: true })}>
                    <h1 className="dashboard-title">200 Success</h1>
                </Content>}
                {dashboard && <Fragment><Content className="dashboard-side">
                    <Sider collapsible collapsed={collapsed} onCollapse={collapsed => this.setState({ collapsed })} width="350">
                        {!collapsed && <Input
                            size="large"
                            placeholder="Search by "
                            onChange={value => console.log(value)}
                            onPressEnter={e => {
                                if (searchBy === "store") dispatch(getStore({ search: e.target.value }))
                                else dispatch(getItem({ search: e.target.value }))
                                this.setState({ view: searchBy })
                            }}
                            style={{ width: 300, margin: '30px auto' }}
                            addonAfter={<Select defaultValue="Store" style={{ width: 80 }} onChange={value => this.setState({ searchBy: value })} >
                                <Option value="store">Store</Option>
                                <Option value="item">Item</Option>
                            </Select>}
                        />}
                        {!collapsed && <Dragger
                            className="upload-dragger"
                            type="file"
                            action="/api/upload"
                        // onChange={info => {
                        //     const { status } = info.file;
                        //     if (status === 'done') console.log(info.file.name);
                        //     else {
                        //         this.setState({ showLoader: true });
                        //         setTimeout(
                        //             () => this.setState({ showDashboard: true }),
                        //             5000
                        //         );                                    
                        //     }
                        // }}
                        >
                            <p className="ant-upload-drag-icon">
                                <Icon type="upload" />
                            </p>
                            <p style={{ color: 'white' }}>
                                Click or drag files to this area to upload
                            </p>
                        </Dragger>}
                        {!collapsed && <div style={{ display: 'flex' }}>
                            {category && category.map(item =>
                                <Card
                                    className="category-card"
                                    bordered={false}
                                    cover={<img src={item.name === "Food" ? food : groceries} style={{ width: '94px', margin: 'auto' }} />}
                                    onClick={() => {
                                        this.setState({ view: 'item' })
                                        dispatch(getItem({ category_id: item.id }))
                                    }}
                                >
                                    <Meta description={item.name} style={{ textAlign: 'center' }} />
                                </Card>)}
                        </div>}
                    </Sider>
                </Content>
                    <Content className="dashboard-main">
                        <div className="dashboard-content">
                            {view === "item" && <Icon type="arrow-left" style={{ fontSize: '20px', color: 'white', marginBottom: '20px' }} onClick={() => this.setState({ view: 'store' })} />}
                            {view === 'store' ?
                                <Row gutter={16}>
                                    {store && store.map(item =>
                                        <Col span={8}>
                                            <Card
                                                className="store-card"
                                                bordered={false}
                                                cover={<Icon type="shop" style={{ fontSize: '40px', margin: '20px auto' }} />}
                                                onClick={() => {
                                                    this.setState({ view: 'item' })
                                                    dispatch(getItem({ id: item.store_id }))
                                                }}
                                            >
                                                <Meta title={item.store_name} description={item.store_address} style={{ textAlign: 'center' }} />
                                            </Card>
                                        </Col>
                                    )}
                                </Row> :
                                <List item={item} itemDetail={itemDetail} getItemDetail={(item) => dispatch(getItemDetail(item))} />
                            }
                        </div>
                    </Content>
                </Fragment>}
            </Layout>
        )
    }
}

export default connect((state) => ({
    store: state.root.get('store'),
    item: state.root.get('item'),
    itemDetail: state.root.get('itemDetail'),
    category: state.root.get('category'),
}))(Dashboard)


